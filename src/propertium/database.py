from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import os
import logging
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, AsyncContextManager
from contextlib import asynccontextmanager

# Set up logger
logger = logging.getLogger(__name__)

# Create base class for models
Base = declarative_base()

class Database:
    def __init__(self, database_url: Optional[str] = None):
        # Get database URL from environment variable or use a default or provided value
        self.database_url = database_url or os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/propertium")
        self.engine = None
        self.session_factory = None
        self._initialize()

    def _initialize(self):
        # Check if SQLite is being used
        if self.database_url.startswith('sqlite'):
            # For SQLite, use aiosqlite as the async driver
            async_db_url = self.database_url.replace('sqlite://', 'sqlite+aiosqlite://')
            # If it's a file-based SQLite database (not in-memory)
            if not async_db_url.endswith(':memory:') and not async_db_url.startswith('sqlite+aiosqlite:////'):
                # Ensure the directory exists
                db_path = async_db_url.replace('sqlite+aiosqlite:///', '')
                os.makedirs(os.path.dirname(db_path), exist_ok=True)
        else:
            # For PostgreSQL, use asyncpg
            async_db_url = self.database_url.replace('postgresql://', 'postgresql+asyncpg://')

        # Create SQLAlchemy async engine
        self.engine = create_async_engine(async_db_url, echo=True)

        # Initialize SpatiaLite for SQLite databases
        if self.database_url.startswith('sqlite'):
            from sqlalchemy import event
            from sqlalchemy.engine import Engine

            @event.listens_for(Engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("SELECT InitSpatialMetaData(1)")
                cursor.close()

        # Create async session factory
        self.session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            class_=AsyncSession
        )

    @asynccontextmanager
    async def session(self) -> AsyncContextManager[AsyncSession]:
        """
        Get a database session as an async context manager.
        """
        session = self.session_factory()
        try:
            yield session
        finally:
            await session.close()

    async def close(self) -> None:
        """
        Close the database engine and all connections.
        """
        if self.engine:
            await self.engine.dispose()

    async def check_health(self):
        """
        Check if the database is alive and responsive by executing a simple query.
        Returns a tuple (is_healthy, error_message)
        """
        try:
            # Create a new session
            async with self.session() as db:
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

# Create default database instance
db = Database()

# Dependency to get DB session
async def get_db():
    async with db.session() as session:
        try:
            yield session
        finally:
            pass  # Session is automatically closed by the context manager


def change_db(newConnection:Database):
    global db
    db = newConnection