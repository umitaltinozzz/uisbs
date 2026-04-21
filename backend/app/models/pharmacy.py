"""
Pharmacy model for UISBS application.
Handles pharmacy information and location data with PostGIS support.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Float, Integer, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography
import uuid
import enum

from ..core.database import Base


class PharmacyStatusEnum(enum.Enum):
    """Enum for pharmacy status."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"


class Pharmacy(Base):
    """
    Pharmacy model for storing pharmacy information and location.
    Uses PostGIS for geographic data storage and queries.
    """
    __tablename__ = "pharmacies"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Basic information
    name = Column(String(200), nullable=False, index=True)
    license_number = Column(String(50), unique=True, nullable=False, index=True)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(255), nullable=True)
    website = Column(String(500), nullable=True)
    
    # Address information
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False, index=True)
    district = Column(String(100), nullable=False, index=True)
    postal_code = Column(String(10), nullable=True)
    
    # Geographic location (PostGIS)
    location = Column(Geography('POINT', srid=4326), nullable=False, index=True)
    
    # Operating information
    is_24_hours = Column(Boolean, default=False, nullable=False)
    opening_hours = Column(Text, nullable=True)  # JSON string for complex schedules
    
    # Status and verification
    status = Column(SAEnum(PharmacyStatusEnum), default=PharmacyStatusEnum.PENDING, nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    verification_date = Column(DateTime(timezone=True), nullable=True)
    
    # Additional information
    description = Column(Text, nullable=True)
    services = Column(Text, nullable=True)  # JSON string for services offered
    
    # Ratings and reviews
    average_rating = Column(Float, default=0.0, nullable=False)
    total_reviews = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Foreign keys
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Relationships
    owner = relationship("User", back_populates="pharmacy")
    drug_stocks = relationship("DrugStock", back_populates="pharmacy", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Pharmacy(id={self.id}, name={self.name}, license={self.license_number})>"
    
    @property
    def full_address(self) -> str:
        """Get formatted full address."""
        address_parts = [self.address_line1]
        if self.address_line2:
            address_parts.append(self.address_line2)
        address_parts.extend([self.district, self.city])
        if self.postal_code:
            address_parts.append(self.postal_code)
        return ", ".join(address_parts)
    
    @property
    def is_approved(self) -> bool:
        """Check if pharmacy is approved."""
        return self.status == PharmacyStatusEnum.APPROVED
    
    @property
    def is_pending(self) -> bool:
        """Check if pharmacy is pending approval."""
        return self.status == PharmacyStatusEnum.PENDING
    
    @property
    def is_operational(self) -> bool:
        """Check if pharmacy is operational (approved and active)."""
        return self.is_approved and self.is_active
    
    def get_coordinates(self) -> tuple:
        """Get latitude and longitude coordinates."""
        if self.location:
            # PostGIS returns coordinates as (longitude, latitude)
            coords = self.location.coords(session)
            return (coords[0][1], coords[0][0])  # Return as (lat, lng)
        return (None, None)
    
    def set_coordinates(self, latitude: float, longitude: float):
        """Set geographic coordinates."""
        from geoalchemy2.elements import WKTElement
        self.location = WKTElement(f'POINT({longitude} {latitude})', srid=4326)
    
    def approve(self):
        """Approve pharmacy."""
        self.status = PharmacyStatusEnum.APPROVED
        self.verification_date = func.now()
    
    def reject(self):
        """Reject pharmacy."""
        self.status = PharmacyStatusEnum.REJECTED
    
    def suspend(self):
        """Suspend pharmacy."""
        self.status = PharmacyStatusEnum.SUSPENDED
        self.is_active = False
    
    def activate(self):
        """Activate pharmacy."""
        if self.is_approved:
            self.is_active = True
    
    def deactivate(self):
        """Deactivate pharmacy."""
        self.is_active = False 