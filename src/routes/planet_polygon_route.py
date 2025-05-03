from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from services.planet_polygon_service import PlanetPolygonService
from schemas.planet_polygon import PlanetPolygonResponse, PlanetPolygonCreate

router = APIRouter()

@router.get("/", response_model=List[PlanetPolygonResponse])
async def get_polygons(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Retrieve planet polygons with pagination.
    """
    polygons = await PlanetPolygonService.get_polygons(db, skip, limit)
    return [PlanetPolygonResponse.from_orm(polygon) for polygon in polygons]

@router.get("/{osm_id}", response_model=PlanetPolygonResponse)
async def get_polygon(osm_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a specific planet polygon by OSM ID.
    """
    polygon = await PlanetPolygonService.get_polygon_by_osm_id(db, osm_id)
    if polygon is None:
        raise HTTPException(status_code=404, detail="Polygon not found")
    return PlanetPolygonResponse.from_orm(polygon)

@router.post("/", response_model=PlanetPolygonResponse)
async def create_polygon(polygon: PlanetPolygonCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new planet polygon.
    """
    db_polygon = await PlanetPolygonService.create_polygon(db, polygon)
    return PlanetPolygonResponse.from_orm(db_polygon)

@router.post("/bulk", response_model=List[PlanetPolygonResponse])
async def bulk_insert_polygons(polygons: List[PlanetPolygonCreate], db: AsyncSession = Depends(get_db)):
    """
    Insert multiple planet polygons at once.
    """
    db_polygons = await PlanetPolygonService.bulk_insert_polygons(db, polygons)
    return [PlanetPolygonResponse.from_orm(polygon) for polygon in db_polygons]
