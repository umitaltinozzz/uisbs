"""
Core configuration settings for UISBS application.
Handles environment variables and application settings.
"""

from typing import Optional, List
from pydantic import field_validator
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    APP_NAME: str = "UISBS - Ulusal İlaç Stok Takip Sistemi"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://uisbs:uisbs123@localhost/uisbs_db"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "application/pdf"]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Audit
    AUDIT_LOG_RETENTION_DAYS: int = 365
    
    model_config = {"env_file": ".env", "case_sensitive": True}


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Constants for the application
class UserRoles:
    """User role constants."""
    ADMIN = "admin"
    PHARMACY = "pharmacy"
    CITIZEN = "citizen"
    GOVERNMENT_OFFICIAL = "government_official"


class AuditActions:
    """Audit action constants."""
    LOGIN = "login"
    LOGOUT = "logout"
    STOCK_UPDATE = "stock_update"
    STOCK_CREATE = "stock_create"
    STOCK_DELETE = "stock_delete"
    USER_CREATE = "user_create"
    USER_UPDATE = "user_update"
    USER_DELETE = "user_delete"
    PHARMACY_APPROVE = "pharmacy_approve"
    PHARMACY_REJECT = "pharmacy_reject"


class DrugCategories:
    """Drug category constants."""
    PRESCRIPTION = "prescription"
    OTC = "otc"  # Over-the-counter
    CONTROLLED = "controlled"
    EMERGENCY = "emergency"


# Application metadata
APP_METADATA = {
    "title": "UISBS API",
    "description": """
    Ulusal İlaç Stok Takip ve Dağıtım Veri Sistemi (UISBS) API
    
    Bu sistem Türkiye'deki eczanelerin ilaç stoklarını merkezi olarak takip eder
    ve vatandaşların ilaç erişimini kolaylaştırır.
    
    ## Özellikler
    
    * **Eczane Stok Yönetimi**: Eczaneler stoklarını gerçek zamanlı güncelleyebilir
    * **Vatandaş Arama**: Lokasyon bazlı ilaç arama
    * **Güvenli Erişim**: JWT tabanlı kimlik doğrulama
    * **Audit Logging**: Tüm kritik işlemler loglanır
    * **KVKK Uyumu**: Kişisel veri koruma standartlarına uygun
    """,
    "version": "1.0.0",
    "contact": {
        "name": "UISBS Geliştirici Ekibi",
        "email": "dev@uisbs.gov.tr",
    },
    "license_info": {
        "name": "Kamu Lisansı",
        "url": "https://uisbs.gov.tr/license",
    },
} 