"""
Database configuration and session management for UISBS.
Handles PostgreSQL connection with PostGIS support.
"""

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.pool import QueuePool
from typing import Generator
import logging

from .config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# Database engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,  # Verify connections before use
    echo=settings.DEBUG,  # Log SQL queries in debug mode
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Naming convention for constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

Base.metadata = MetaData(naming_convention=convention)


def get_database_session() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    Ensures proper session cleanup after request.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def create_database_tables():
    """Create all database tables."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def check_database_connection() -> bool:
    """
    Check if database connection is working.
    Returns True if connection is successful, False otherwise.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False


def enable_postgis_extension():
    """Enable PostGIS extension for geographic data support."""
    try:
        with engine.connect() as connection:
            connection.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
            connection.execute(text("CREATE EXTENSION IF NOT EXISTS postgis_topology"))
            connection.commit()
        logger.info("PostGIS extension enabled successfully")
    except Exception as e:
        logger.error(f"Error enabling PostGIS extension: {e}")
        raise


# Database health check function
async def database_health_check() -> dict:
    """
    Perform database health check.
    Returns status information about database connection.
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version(), now()"))
            row = result.fetchone()
            
            return {
                "status": "healthy",
                "database_version": row[0] if row else "unknown",
                "current_time": row[1].isoformat() if row else "unknown",
                "pool_size": engine.pool.size(),
                "checked_out_connections": engine.pool.checkedout(),
            }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "pool_size": 0,
            "checked_out_connections": 0,
        } 