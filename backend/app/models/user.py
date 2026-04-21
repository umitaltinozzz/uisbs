"""
User model for UISBS application.
Handles user authentication and role-based access control.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, Enum as SAEnum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from ..core.database import Base
from ..core.config import UserRoles


class UserRoleEnum(enum.Enum):
    """Enum for user roles."""
    ADMIN = UserRoles.ADMIN
    PHARMACY = UserRoles.PHARMACY
    CITIZEN = UserRoles.CITIZEN
    GOVERNMENT_OFFICIAL = UserRoles.GOVERNMENT_OFFICIAL


class User(Base):
    """
    User model for authentication and authorization.
    Supports multiple user types with role-based permissions.
    """
    __tablename__ = "users"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Authentication fields
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # User information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=True)
    
    # Role and permissions
    role = Column(SAEnum(UserRoleEnum), nullable=False, index=True)
    
    # Additional information
    profile_picture_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    # Security fields
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    password_reset_token = Column(String(255), nullable=True)
    password_reset_expires = Column(DateTime(timezone=True), nullable=True)
    email_verification_token = Column(String(255), nullable=True)
    
    # Relationships
    pharmacy = relationship("Pharmacy", back_populates="owner", uselist=False)
    audit_logs = relationship("AuditLog", back_populates="user")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role.value})>"
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_admin(self) -> bool:
        """Check if user is admin."""
        return self.role == UserRoleEnum.ADMIN
    
    @property
    def is_pharmacy_owner(self) -> bool:
        """Check if user is pharmacy owner."""
        return self.role == UserRoleEnum.PHARMACY
    
    @property
    def is_citizen(self) -> bool:
        """Check if user is citizen."""
        return self.role == UserRoleEnum.CITIZEN
    
    @property
    def is_government_official(self) -> bool:
        """Check if user is government official."""
        return self.role == UserRoleEnum.GOVERNMENT_OFFICIAL
    
    @property
    def can_manage_stocks(self) -> bool:
        """Check if user can manage drug stocks."""
        return self.role in [UserRoleEnum.ADMIN, UserRoleEnum.PHARMACY]
    
    @property
    def can_view_all_data(self) -> bool:
        """Check if user can view all system data."""
        return self.role in [UserRoleEnum.ADMIN, UserRoleEnum.GOVERNMENT_OFFICIAL]
    
    def is_account_locked(self) -> bool:
        """Check if account is locked due to failed login attempts."""
        if self.locked_until is None:
            return False
        return self.locked_until > func.now()
    
    def reset_failed_login_attempts(self):
        """Reset failed login attempts counter."""
        self.failed_login_attempts = 0
        self.locked_until = None
    
    def increment_failed_login_attempts(self):
        """Increment failed login attempts and lock account if necessary."""
        self.failed_login_attempts += 1
        
        # Lock account after 5 failed attempts for 30 minutes
        if self.failed_login_attempts >= 5:
            from datetime import datetime, timedelta
            self.locked_until = datetime.utcnow() + timedelta(minutes=30) 