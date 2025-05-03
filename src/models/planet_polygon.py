from sqlalchemy import Column, Integer, String, Float, Boolean, Text, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry
from sqlalchemy.types import TypeDecorator
import json

from database import Base

# Custom JSON type for Map<String, String>
class JSONMap(TypeDecorator):
    impl = JSONB
    
    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return None
        
    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return None

class PlanetPolygon(Base):
    __tablename__ = "fct_planet_polygons"
    
    osm_id = Column(BigInteger, primary_key=True, index=True)
    admin_level = Column(Text)
    boundary = Column(Text)
    name = Column(Text)
    z_order = Column(Integer)
    way_area = Column(Float)
    way = Column(Geometry('GEOMETRY', srid=3857), nullable=True, index=True)
    tags = Column(JSONMap)
    country = Column(String(2), nullable=True, index=True)
    
    avr_rent_price = Column(Float, nullable=True)
    avr_rent_price_per_m = Column(Float, nullable=True)
    avr_sale_price = Column(Float, nullable=True)
    avr_sale_price_per_m = Column(Float, nullable=True)
    is_city_for_search = Column(Boolean, nullable=True, index=True)
    
    name_en = Column(Text, nullable=True)
    code = Column(Text, nullable=True)
    alpha2 = Column(Text, nullable=True)
    border_type = Column(Text, nullable=True)