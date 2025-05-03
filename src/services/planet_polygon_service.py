from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from geoalchemy2.functions import ST_Transform, ST_SetSRID, ST_Point, ST_Contains

from models.planet_polygon import PlanetPolygon
from schemas.geo_point import GeoPoint

class PlanetPolygonService:
    @staticmethod
    async def get_polygon_by_osm_id(db: AsyncSession, osm_id: int) -> Optional[PlanetPolygon]:
        """
        Retrieve a specific planet polygon by OSM ID.
        """
        result = await db.execute(select(PlanetPolygon).filter(PlanetPolygon.osm_id == osm_id))
        return result.scalars().first()

    @staticmethod
    async def find_by_point(db: AsyncSession, geo_point: GeoPoint) -> List[PlanetPolygon]:
        """
        Find all polygons that contain the given point.
        """
        # Create a point geometry from the lat/lng
        point = ST_Transform(
            ST_SetSRID(
                ST_Point(geo_point.lng, geo_point.lat),
                geo_point.srid
            ),
            3857  # Transform to the same SRID as the way column
        )

        # Find polygons that contain the point
        query = select(PlanetPolygon).filter(
            func.ST_Contains(PlanetPolygon.way, point)
        )

        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_countries(db: AsyncSession) -> List[PlanetPolygon]:
        """
        Get all countries (polygons with admin_level = 2).
        """
        query = select(PlanetPolygon).filter(PlanetPolygon.admin_level == "2")
        result = await db.execute(query)
        return result.scalars().all()
