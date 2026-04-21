"""
Authentication endpoints for UISBS application.
Handles user login, logout, token refresh, and password management.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import structlog

from ....core.database import get_database_session
from ....core.config import get_settings
from ....models.user import User
from ....models.audit_log import AuditLog, AuditActionEnum
from ....schemas.user import UserLogin, Token, UserPasswordReset, UserPasswordResetConfirm, UserPasswordChange
from ....services.auth_service import AuthService
from ....services.audit_service import AuditService
from ....utils.security import get_current_user, get_current_active_user

router = APIRouter()
logger = structlog.get_logger()
settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@router.post("/login", response_model=Token)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_database_session)
):
    """
    User login endpoint.
    Authenticates user and returns JWT tokens.
    """
    auth_service = AuthService(db)
    audit_service = AuditService(db)
    
    try:
        # Authenticate user
        user = auth_service.authenticate_user(form_data.username, form_data.password)
        
        if not user:
            # Log failed login attempt
            await audit_service.log_action(
                action=AuditActionEnum.LOGIN,
                resource_type="user",
                result="failure",
                user_email=form_data.username,
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent"),
                error_message="Invalid credentials"
            )
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if account is locked
        if user.is_account_locked():
            await audit_service.log_action(
                action=AuditActionEnum.LOGIN,
                resource_type="user",
                result="failure",
                user_id=str(user.id),
                user_email=user.email,
                user_role=user.role.value,
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent"),
                error_message="Account locked due to failed login attempts"
            )
            
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail="Account is locked due to multiple failed login attempts",
            )
        
        # Check if user is active
        if not user.is_active:
            await audit_service.log_action(
                action=AuditActionEnum.LOGIN,
                resource_type="user",
                result="failure",
                user_id=str(user.id),
                user_email=user.email,
                user_role=user.role.value,
                ip_address=request.client.host if request.client else None,
                user_agent=request.headers.get("user-agent"),
                error_message="Account is inactive"
            )
            
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive",
            )
        
        # Generate tokens
        access_token = auth_service.create_access_token(
            data={"sub": user.email, "user_id": str(user.id), "role": user.role.value}
        )
        refresh_token = auth_service.create_refresh_token(
            data={"sub": user.email, "user_id": str(user.id)}
        )
        
        # Update user login information
        user.last_login_at = datetime.utcnow()
        user.reset_failed_login_attempts()
        db.commit()
        
        # Log successful login
        await audit_service.log_action(
            action=AuditActionEnum.LOGIN,
            resource_type="user",
            result="success",
            user_id=str(user.id),
            user_email=user.email,
            user_role=user.role.value,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        
        logger.info(
            "User logged in successfully",
            user_id=str(user.id),
            email=user.email,
            role=user.role.value
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Login error", error=str(e), email=form_data.username)
        
        # Log error
        await audit_service.log_action(
            action=AuditActionEnum.LOGIN,
            resource_type="user",
            result="error",
            user_email=form_data.username,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            error_message=str(e)
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed due to server error"
        )


@router.post("/logout")
async def logout(
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database_session)
):
    """
    User logout endpoint.
    Logs the logout action for audit purposes.
    """
    audit_service = AuditService(db)
    
    try:
        # Log logout action
        await audit_service.log_action(
            action=AuditActionEnum.LOGOUT,
            resource_type="user",
            result="success",
            user_id=str(current_user.id),
            user_email=current_user.email,
            user_role=current_user.role.value,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        
        logger.info(
            "User logged out successfully",
            user_id=str(current_user.id),
            email=current_user.email
        )
        
        return {"message": "Successfully logged out"}
        
    except Exception as e:
        logger.error("Logout error", error=str(e), user_id=str(current_user.id))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed due to server error"
        )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: Request,
    refresh_token: str,
    db: Session = Depends(get_database_session)
):
    """
    Refresh access token using refresh token.
    """
    auth_service = AuthService(db)
    
    try:
        # Verify refresh token and get user
        user = auth_service.verify_refresh_token(refresh_token)
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Generate new tokens
        access_token = auth_service.create_access_token(
            data={"sub": user.email, "user_id": str(user.id), "role": user.role.value}
        )
        new_refresh_token = auth_service.create_refresh_token(
            data={"sub": user.email, "user_id": str(user.id)}
        )
        
        logger.info(
            "Token refreshed successfully",
            user_id=str(user.id),
            email=user.email
        )
        
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Token refresh error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.post("/change-password")
async def change_password(
    request: Request,
    password_data: UserPasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database_session)
):
    """
    Change user password.
    """
    auth_service = AuthService(db)
    audit_service = AuditService(db)
    
    try:
        # Verify current password
        if not auth_service.verify_password(password_data.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Update password
        current_user.hashed_password = auth_service.get_password_hash(password_data.new_password)
        db.commit()
        
        # Log password change
        await audit_service.log_action(
            action=AuditActionEnum.USER_UPDATE,
            resource_type="user",
            resource_id=str(current_user.id),
            result="success",
            user_id=str(current_user.id),
            user_email=current_user.email,
            user_role=current_user.role.value,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            changes_summary="Password changed"
        )
        
        logger.info(
            "Password changed successfully",
            user_id=str(current_user.id),
            email=current_user.email
        )
        
        return {"message": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Password change error", error=str(e), user_id=str(current_user.id))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed"
        )


@router.post("/forgot-password")
async def forgot_password(
    request: Request,
    password_reset: UserPasswordReset,
    db: Session = Depends(get_database_session)
):
    """
    Request password reset.
    """
    auth_service = AuthService(db)
    
    try:
        # Generate password reset token
        reset_token = auth_service.create_password_reset_token(password_reset.email)
        
        # In a real application, you would send this token via email
        # For now, we'll just return a success message
        
        logger.info(
            "Password reset requested",
            email=password_reset.email,
            ip_address=request.client.host if request.client else None
        )
        
        return {"message": "Password reset instructions sent to your email"}
        
    except Exception as e:
        logger.error("Password reset request error", error=str(e), email=password_reset.email)
        # Don't reveal if email exists or not for security
        return {"message": "Password reset instructions sent to your email"}


@router.get("/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user information.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "role": current_user.role.value,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "created_at": current_user.created_at,
        "last_login_at": current_user.last_login_at
    } 