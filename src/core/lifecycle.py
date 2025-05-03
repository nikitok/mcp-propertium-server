from contextlib import asynccontextmanager
from fastapi import FastAPI, Body
import logging
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info("Starting application...")

    yield
    logger.info("Shutting down application...")
