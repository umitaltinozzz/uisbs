"""Audit service stub."""

from sqlalchemy.orm import Session
from typing import Optional

from ..models.audit_log import AuditLog, AuditActionEnum


class AuditService:
    def __init__(self, db: Session):
        self.db = db

    async def log_action(
        self,
        action: AuditActionEnum,
        resource_type: str,
        result: str = "success",
        user_id: Optional[str] = None,
        user_email: Optional[str] = None,
        user_role: Optional[str] = None,
        resource_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        error_message: Optional[str] = None,
        changes_summary: Optional[str] = None,
        **kwargs
    ):
        try:
            log = AuditLog.create_log(
                action=action,
                resource_type=resource_type,
                result=result,
                user_id=user_id,
                user_email=user_email,
                user_role=user_role,
                resource_id=resource_id,
                ip_address=ip_address,
                user_agent=user_agent,
                error_message=error_message,
                changes_summary=changes_summary,
            )
            self.db.add(log)
            self.db.commit()
        except Exception:
            self.db.rollback()
