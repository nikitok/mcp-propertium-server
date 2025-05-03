from fastapi import FastAPI, Body, HTTPException
import uvicorn

from core.lifecycle import lifespan
from core.logger import setup_logging
from routes.openai_route import router as openai_router
from routes.planet_polygon_route import router as planet_polygon_router
from routes.health_route import router as health_router

setup_logging()


fastAPI = FastAPI(
    title="RestAPI + MCP server for OSM and Propertium data",
    description="RestAPI + MCP server for OSM and Propertium data",
    version="1.0.0",
    lifespan=lifespan
)

@fastAPI.get("/")
async def root():
    return {"message": "i am live"}


fastAPI.include_router(openai_router, prefix="/openai", tags=["OpenAI Processing"])
fastAPI.include_router(planet_polygon_router, prefix="/planet-polygons", tags=["Planet Polygons"])
fastAPI.include_router(health_router, prefix="/health")

