import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient

from propertium.main import app
from propertium.schemas.health_schemas import HealthStatus

pytestmark = pytest.mark.asyncio
pytest.mark.asyncio_mode = "auto"


@pytest.mark.asyncio
async def test_health_live_check():
    """Test the health/live check endpoint returns correct status."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/health/live")
        assert response.status_code == 200

        # The status can be either ALIVE or UNHEALTHY depending on the database connection
        status = response.json()["status"]
        assert status in [HealthStatus.ALIVE.value, HealthStatus.UNHEALTHY.value]

        # Check database status
        db_status = response.json()["database"]["status"]
        if status == HealthStatus.ALIVE.value:
            assert db_status == "healthy"
        else:
            assert db_status == "unhealthy"
            # If unhealthy, there should be an error message
            assert "error" in response.json()["database"]
