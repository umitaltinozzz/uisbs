"""
Drug and DrugStock models for UISBS application.
Handles drug information and pharmacy stock management.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Float, Integer, Numeric, Date, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from ..core.database import Base
from ..core.config import DrugCategories


class DrugCategoryEnum(enum.Enum):
    """Enum for drug categories."""
    PRESCRIPTION = DrugCategories.PRESCRIPTION
    OTC = DrugCategories.OTC
    CONTROLLED = DrugCategories.CONTROLLED
    EMERGENCY = DrugCategories.EMERGENCY


class Drug(Base):
    """
    Drug model for storing drug information.
    Contains master data for all drugs in the system.
    """
    __tablename__ = "drugs"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Drug identification
    barcode = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    generic_name = Column(String(255), nullable=True, index=True)
    brand_name = Column(String(255), nullable=True)
    
    # Drug details
    active_ingredient = Column(String(500), nullable=False)
    strength = Column(String(100), nullable=True)  # e.g., "500mg", "10mg/ml"
    dosage_form = Column(String(100), nullable=True)  # e.g., "tablet", "syrup", "injection"
    package_size = Column(String(100), nullable=True)  # e.g., "30 tablets", "100ml"
    
    # Classification
    category = Column(SAEnum(DrugCategoryEnum), nullable=False, index=True)
    atc_code = Column(String(20), nullable=True, index=True)  # Anatomical Therapeutic Chemical code
    
    # Manufacturer information
    manufacturer = Column(String(255), nullable=False, index=True)
    manufacturer_country = Column(String(100), nullable=True)
    
    # Regulatory information
    license_number = Column(String(100), nullable=True)
    is_approved = Column(Boolean, default=True, nullable=False)
    approval_date = Column(Date, nullable=True)
    
    # Additional information
    description = Column(Text, nullable=True)
    indications = Column(Text, nullable=True)  # What the drug is used for
    contraindications = Column(Text, nullable=True)  # When not to use
    side_effects = Column(Text, nullable=True)
    storage_conditions = Column(Text, nullable=True)
    
    # Pricing (reference price)
    reference_price = Column(Numeric(10, 2), nullable=True)
    currency = Column(String(3), default="TRY", nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    stocks = relationship("DrugStock", back_populates="drug", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Drug(id={self.id}, name={self.name}, barcode={self.barcode})>"
    
    @property
    def full_name(self) -> str:
        """Get full drug name with strength."""
        if self.strength:
            return f"{self.name} {self.strength}"
        return self.name
    
    @property
    def is_prescription_required(self) -> bool:
        """Check if drug requires prescription."""
        return self.category in [DrugCategoryEnum.PRESCRIPTION, DrugCategoryEnum.CONTROLLED]
    
    @property
    def is_controlled_substance(self) -> bool:
        """Check if drug is controlled substance."""
        return self.category == DrugCategoryEnum.CONTROLLED


class DrugStock(Base):
    """
    DrugStock model for tracking drug inventory in pharmacies.
    Links drugs to pharmacies with quantity and expiry information.
    """
    __tablename__ = "drug_stocks"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign keys
    drug_id = Column(UUID(as_uuid=True), ForeignKey("drugs.id"), nullable=False, index=True)
    pharmacy_id = Column(UUID(as_uuid=True), ForeignKey("pharmacies.id"), nullable=False, index=True)
    
    # Stock information
    quantity = Column(Integer, nullable=False, default=0)
    reserved_quantity = Column(Integer, nullable=False, default=0)  # Reserved for prescriptions
    minimum_stock_level = Column(Integer, nullable=False, default=5)
    
    # Batch information
    batch_number = Column(String(100), nullable=True)
    expiry_date = Column(Date, nullable=False, index=True)
    manufacturing_date = Column(Date, nullable=True)
    
    # Pricing
    purchase_price = Column(Numeric(10, 2), nullable=True)
    selling_price = Column(Numeric(10, 2), nullable=False)
    discount_percentage = Column(Float, default=0.0, nullable=False)
    
    # Status
    is_available = Column(Boolean, default=True, nullable=False)
    is_expired = Column(Boolean, default=False, nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Relationships
    drug = relationship("Drug", back_populates="stocks")
    pharmacy = relationship("Pharmacy", back_populates="drug_stocks")
    updated_by_user = relationship("User", foreign_keys=[last_updated_by])
    
    def __repr__(self) -> str:
        return f"<DrugStock(id={self.id}, drug_id={self.drug_id}, pharmacy_id={self.pharmacy_id}, quantity={self.quantity})>"
    
    @property
    def available_quantity(self) -> int:
        """Get available quantity (total - reserved)."""
        return max(0, self.quantity - self.reserved_quantity)
    
    @property
    def is_low_stock(self) -> bool:
        """Check if stock is below minimum level."""
        return self.quantity <= self.minimum_stock_level
    
    @property
    def is_out_of_stock(self) -> bool:
        """Check if completely out of stock."""
        return self.quantity <= 0
    
    @property
    def days_until_expiry(self) -> int:
        """Get number of days until expiry."""
        from datetime import date
        if self.expiry_date:
            delta = self.expiry_date - date.today()
            return delta.days
        return 0
    
    @property
    def is_expiring_soon(self) -> bool:
        """Check if drug is expiring within 30 days."""
        return self.days_until_expiry <= 30
    
    @property
    def final_price(self) -> float:
        """Get final selling price after discount."""
        if self.discount_percentage > 0:
            return float(self.selling_price) * (1 - self.discount_percentage / 100)
        return float(self.selling_price)
    
    def update_quantity(self, new_quantity: int, user_id: str = None):
        """Update stock quantity with audit trail."""
        old_quantity = self.quantity
        self.quantity = max(0, new_quantity)
        self.last_updated_by = user_id
        self.updated_at = func.now()
        
        # Check if expired
        from datetime import date
        if self.expiry_date and self.expiry_date <= date.today():
            self.is_expired = True
            self.is_available = False
    
    def reserve_quantity(self, quantity: int) -> bool:
        """Reserve quantity for prescription. Returns True if successful."""
        if self.available_quantity >= quantity:
            self.reserved_quantity += quantity
            return True
        return False
    
    def release_reservation(self, quantity: int):
        """Release reserved quantity."""
        self.reserved_quantity = max(0, self.reserved_quantity - quantity)
    
    def sell_quantity(self, quantity: int) -> bool:
        """Sell quantity (reduce from stock). Returns True if successful."""
        if self.available_quantity >= quantity:
            self.quantity -= quantity
            return True
        return False 