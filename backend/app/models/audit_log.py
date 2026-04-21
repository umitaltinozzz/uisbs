"""
Audit log model for UISBS application.
Tracks all critical operations for security and compliance.
"""

from sqlalchemy import Column, String, DateTime, Text, ForeignKey, JSON, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from ..core.database import Base
from ..core.config import AuditActions


class AuditActionEnum(enum.Enum):
    """Enum for audit actions."""
    LOGIN = AuditActions.LOGIN
    LOGOUT = AuditActions.LOGOUT
    STOCK_UPDATE = AuditActions.STOCK_UPDATE
    STOCK_CREATE = AuditActions.STOCK_CREATE
    STOCK_DELETE = AuditActions.STOCK_DELETE
    USER_CREATE = AuditActions.USER_CREATE
    USER_UPDATE = AuditActions.USER_UPDATE
    USER_DELETE = AuditActions.USER_DELETE
    PHARMACY_APPROVE = AuditActions.PHARMACY_APPROVE
    PHARMACY_REJECT = AuditActions.PHARMACY_REJECT


class AuditLog(Base):
    """
    Audit log model for tracking all critical system operations.
    Provides complete audit trail for security and compliance.
    """
    __tablename__ = "audit_logs"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Action information
    action = Column(SAEnum(AuditActionEnum), nullable=False, index=True)
    resource_type = Column(String(100), nullable=False, index=True)  # e.g., "user", "pharmacy", "drug_stock"
    resource_id = Column(String(255), nullable=True, index=True)  # ID of the affected resource
    
    # User information
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    user_email = Column(String(255), nullable=True)  # Stored for audit even if user is deleted
    user_role = Column(String(50), nullable=True)
    
    # Request information
    ip_address = Column(String(45), nullable=True, index=True)  # IPv6 support
    user_agent = Column(Text, nullable=True)
    request_method = Column(String(10), nullable=True)  # GET, POST, PUT, DELETE
    request_path = Column(String(500), nullable=True)
    
    # Change information
    old_values = Column(JSON, nullable=True)  # Previous state
    new_values = Column(JSON, nullable=True)  # New state
    changes_summary = Column(Text, nullable=True)  # Human-readable summary
    
    # Result information
    result = Column(String(20), nullable=False, index=True)  # success, failure, error
    error_message = Column(Text, nullable=True)
    
    # Additional context
    session_id = Column(String(255), nullable=True, index=True)
    correlation_id = Column(String(255), nullable=True, index=True)  # For tracking related operations
    additional_data = Column(JSON, nullable=True)  # Any additional context
    
    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, action={self.action.value}, user_id={self.user_id}, timestamp={self.timestamp})>"
    
    @classmethod
    def create_log(
        cls,
        action: AuditActionEnum,
        resource_type: str,
        result: str = "success",
        user_id: str = None,
        user_email: str = None,
        user_role: str = None,
        resource_id: str = None,
        ip_address: str = None,
        user_agent: str = None,
        request_method: str = None,
        request_path: str = None,
        old_values: dict = None,
        new_values: dict = None,
        changes_summary: str = None,
        error_message: str = None,
        session_id: str = None,
        correlation_id: str = None,
        additional_data: dict = None
    ) -> "AuditLog":
        """
        Create a new audit log entry.
        Factory method for consistent audit log creation.
        """
        return cls(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            user_email=user_email,
            user_role=user_role,
            ip_address=ip_address,
            user_agent=user_agent,
            request_method=request_method,
            request_path=request_path,
            old_values=old_values,
            new_values=new_values,
            changes_summary=changes_summary,
            result=result,
            error_message=error_message,
            session_id=session_id,
            correlation_id=correlation_id,
            additional_data=additional_data
        )
    
    @property
    def is_successful(self) -> bool:
        """Check if the audited action was successful."""
        return self.result == "success"
    
    @property
    def is_security_relevant(self) -> bool:
        """Check if this is a security-relevant action."""
        security_actions = [
            AuditActionEnum.LOGIN,
            AuditActionEnum.LOGOUT,
            AuditActionEnum.USER_CREATE,
            AuditActionEnum.USER_UPDATE,
            AuditActionEnum.USER_DELETE,
            AuditActionEnum.PHARMACY_APPROVE,
            AuditActionEnum.PHARMACY_REJECT
        ]
        return self.action in security_actions
    
    @property
    def is_data_change(self) -> bool:
        """Check if this action involved data changes."""
        return self.old_values is not None or self.new_values is not None
    
    def get_change_description(self) -> str:
        """Get a human-readable description of changes made."""
        if self.changes_summary:
            return self.changes_summary
        
        if not self.is_data_change:
            return f"{self.action.value} performed on {self.resource_type}"
        
        changes = []
        if self.old_values and self.new_values:
            for key in self.new_values:
                if key in self.old_values and self.old_values[key] != self.new_values[key]:
                    changes.append(f"{key}: {self.old_values[key]} → {self.new_values[key]}")
                elif key not in self.old_values:
                    changes.append(f"{key}: added with value {self.new_values[key]}")
        
        return "; ".join(changes) if changes else "No specific changes recorded" 