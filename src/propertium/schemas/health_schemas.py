from pydantic import BaseModel
from typing import Optional
from enum import Enum

class HealthStatus(str, Enum):
    ALIVE = "alive"
    UNHEALTHY = "unhealthy"
    HEALTHY = "healthy"

class DatabaseStatus(BaseModel):
    status: str
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str

class HealthLiveReadyResponse(BaseModel):
    status: HealthStatus
    database: DatabaseStatus
