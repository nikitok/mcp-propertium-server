from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping

class PlanetPolygonBase(BaseModel):
    id: int
    admin_level: str
    boundary: str
    name: str
    z_order: int
    way_area: float
    tags: Dict[str, str]
    country: Optional[str] = None

    avr_rent_price: Optional[float] = None
    avr_rent_price_per_m: Optional[float] = None
    avr_sale_price: Optional[float] = None
    avr_sale_price_per_m: Optional[float] = None
    is_city_for_search: Optional[bool] = None

    name_en: Optional[str] = None
    code: Optional[str] = None
    alpha2: Optional[str] = None
    border_type: Optional[str] = None

class PlanetPolygonCreate(PlanetPolygonBase):
    osm_id: int
    way: Optional[Dict[str, Any]] = None  # GeoJSON representation

class PlanetPolygonResponse(PlanetPolygonBase):
    osm_id: int
    way: Optional[Dict[str, Any]] = None  # GeoJSON representation

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        # Convert SQLAlchemy model to Pydantic model
        d = {c: getattr(obj, c) for c in obj.__table__.columns.keys()}

        # Convert Geometry to GeoJSON if it exists
        if obj.way is not None:
            shape = to_shape(obj.way)
            d['way'] = mapping(shape)

        return cls(**d)
