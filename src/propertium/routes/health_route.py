from fastapi import APIRouter, HTTPException
import logging
from propertium.database import check_db_health
from propertium.schemas.health_schemas import HealthResponse, HealthLiveReadyResponse, DatabaseStatus, HealthStatus

# Set up logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(tags=["Health Check"])

@router.get("", response_model=HealthResponse)
async def health():
    """
    Simple health check endpoint that returns a healthy status.
    """
    return HealthResponse(status="healthy")

@router.get("/live", response_model=HealthLiveReadyResponse)
async def health_live():
    """
    Health check endpoint to verify if the service is alive.
    Also checks if the database connection is alive.
    """
    try:
        # Check database health
        db_healthy, db_error = await check_db_health()

        if not db_healthy:
            error_response = HealthLiveReadyResponse(
                status=HealthStatus.UNHEALTHY,
                database=DatabaseStatus(
                    status="unhealthy",
                    error=db_error
                )
            )
            logger.error(f"Health live check failed: {db_error}")
            return error_response

        return HealthLiveReadyResponse(
            status=HealthStatus.ALIVE,
            database=DatabaseStatus(
                status="healthy"
            )
        )
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Health live check failed with unexpected error: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {error_msg}")

@router.get("/ready", response_model=HealthLiveReadyResponse)
async def health_ready():
    """
    Health check endpoint to verify if the service is alive.
    Also checks if the database connection is alive.
    """
    try:
        # Check database health
        db_healthy, db_error = await check_db_health()

        if not db_healthy:
            error_response = HealthLiveReadyResponse(
                status=HealthStatus.UNHEALTHY,
                database=DatabaseStatus(
                    status="unhealthy",
                    error=db_error
                )
            )
            logger.error(f"Health ready check failed: {db_error}")
            return error_response

        return HealthLiveReadyResponse(
            status=HealthStatus.ALIVE,
            database=DatabaseStatus(
                status="healthy"
            )
        )
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Health ready check failed with unexpected error: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {error_msg}")
