from fastapi import FastAPI, Body, HTTPException
import uvicorn

from propertium.core.lifecycle import lifespan
from propertium.core.logger import setup_logging
from propertium.routes.openai_route import router as openai_router
from propertium.routes.planet_polygon_route import router as planet_polygon_router
from propertium.routes.health_route import router as health_router

setup_logging()

app = FastAPI(
    title="RestAPI + MCP server for OSM and Propertium data",
    description="RestAPI + MCP server for OSM and Propertium data",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "olá"}


app.include_router(openai_router, prefix="/openai", tags=["OpenAI Processing"])
app.include_router(planet_polygon_router, prefix="/planet-polygons", tags=["Planet Polygons"])
app.include_router(health_router, prefix="/health")

