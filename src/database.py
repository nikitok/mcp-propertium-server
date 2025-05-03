from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import os
import logging
from sqlalchemy.exc import SQLAlchemyError

# Set up logger
logger = logging.getLogger(__name__)

# Get database URL from environment variable or use a default
# Note: For async SQLAlchemy, we need to use postgresql+asyncpg:// instead of postgresql://
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/propertium")
ASYNC_DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://')

# Create SQLAlchemy async engine
engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

# Create async session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

# Create base class for models
Base = declarative_base()

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

# Function to check database health
async def check_db_health():
    """
    Check if the database is alive and responsive by executing a simple query.
    Returns a tuple (is_healthy, error_message)
    """
    try:
        # Create a new session
        async with SessionLocal() as db:
            # Execute a simple query
            await db.execute(text("SELECT 1"))
            return True, None
    except SQLAlchemyError as e:
        error_msg = str(e)
        logger.error(f"Database health check failed with SQLAlchemyError: {error_msg}")
        return False, error_msg
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Database health check failed with unexpected error: {error_msg}")
        return False, error_msg
