from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.planet_polygon import PlanetPolygon
from schemas.planet_polygon import PlanetPolygonCreate, PlanetPolygonResponse

class PlanetPolygonService:
    @staticmethod
    async def get_polygons(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[PlanetPolygon]:
        """
        Retrieve planet polygons with pagination.
        """
        result = await db.execute(select(PlanetPolygon).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def get_polygon_by_osm_id(db: AsyncSession, osm_id: int) -> Optional[PlanetPolygon]:
        """
        Retrieve a specific planet polygon by OSM ID.
        """
        result = await db.execute(select(PlanetPolygon).filter(PlanetPolygon.osm_id == osm_id))
        return result.scalars().first()

    @staticmethod
    async def create_polygon(db: AsyncSession, polygon_data: PlanetPolygonCreate) -> PlanetPolygon:
        """
        Create a new planet polygon.
        """
        db_polygon = PlanetPolygon(
            osm_id=polygon_data.osm_id,
            admin_level=polygon_data.admin_level,
            boundary=polygon_data.boundary,
            name=polygon_data.name,
            z_order=polygon_data.z_order,
            way_area=polygon_data.way_area,
            tags=polygon_data.tags,
            country=polygon_data.country,
            avr_rent_price=polygon_data.avr_rent_price,
            avr_rent_price_per_m=polygon_data.avr_rent_price_per_m,
            avr_sale_price=polygon_data.avr_sale_price,
            avr_sale_price_per_m=polygon_data.avr_sale_price_per_m,
            is_city_for_search=polygon_data.is_city_for_search,
            name_en=polygon_data.name_en,
            code=polygon_data.code,
            alpha2=polygon_data.alpha2,
            border_type=polygon_data.border_type
        )
        
        db.add(db_polygon)
        await db.commit()
        await db.refresh(db_polygon)
        return db_polygon

    @staticmethod
    async def bulk_insert_polygons(db: AsyncSession, polygons_data: List[PlanetPolygonCreate]) -> List[PlanetPolygon]:
        """
        Insert multiple planet polygons at once.
        """
        db_polygons = []
        for polygon_data in polygons_data:
            db_polygon = PlanetPolygon(
                osm_id=polygon_data.osm_id,
                admin_level=polygon_data.admin_level,
                boundary=polygon_data.boundary,
                name=polygon_data.name,
                z_order=polygon_data.z_order,
                way_area=polygon_data.way_area,
                tags=polygon_data.tags,
                country=polygon_data.country,
                avr_rent_price=polygon_data.avr_rent_price,
                avr_rent_price_per_m=polygon_data.avr_rent_price_per_m,
                avr_sale_price=polygon_data.avr_sale_price,
                avr_sale_price_per_m=polygon_data.avr_sale_price_per_m,
                is_city_for_search=polygon_data.is_city_for_search,
                name_en=polygon_data.name_en,
                code=polygon_data.code,
                alpha2=polygon_data.alpha2,
                border_type=polygon_data.border_type
            )
            db_polygons.append(db_polygon)
        
        db.add_all(db_polygons)
        await db.commit()
        
        # Refresh all objects
        for db_polygon in db_polygons:
            await db.refresh(db_polygon)
            
        return db_polygons