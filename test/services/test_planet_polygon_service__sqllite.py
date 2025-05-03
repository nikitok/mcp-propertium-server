import pytest
import os
import sqlite3
import pathlib
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, BigInteger, create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession

from src.propertium.services.planet_polygon_service import PlanetPolygonService
from src.propertium.database import change_db
from src.propertium.database import Database
from src.propertium.database import get_db

# Create a separate test metadata and base
test_metadata = MetaData()
TestBase = declarative_base(metadata=test_metadata)

# Define a test model that matches the structure of PlanetPolygon
class PlanetPolygon(TestBase):
    __tablename__ = "fct_planet_polygons"

    osm_id = Column(BigInteger, primary_key=True, index=True)
    admin_level = Column(Text)
    boundary = Column(Text)
    name = Column(Text)
    z_order = Column(Integer)
    way_area = Column(Float)
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


@pytest.fixture
def sqlite_db_path(tmp_path):
    """Create a temporary path for the SQLite database file."""
    db_file = tmp_path / "test_planet_polygon.db"
    return str(db_file)


@pytest.fixture
async def test_db(sqlite_db_path):
    """Create and configure test database"""
    test_db_path = f"sqlite:///{sqlite_db_path}"
    engine = create_engine(test_db_path)
    test_metadata.create_all(engine)

    # Get the path to init.sql
    current_dir = pathlib.Path(__file__).parent
    init_sql_path = current_dir / "init.sql"

    # Read and execute SQL script
    with open(init_sql_path, "r") as f:
        sql_script = f.read()

    conn = sqlite3.connect(sqlite_db_path)
    conn.executescript(sql_script)
    conn.commit()
    conn.close()

    # Create and return test database instance
    return Database(test_db_path)


@pytest.fixture
async def db_session(test_db):
    """Yield database session"""
    async with test_db.session() as session:
        yield session


@pytest.mark.asyncio
async def test_get_countries_with_real_db(db_session):
    # Теперь db_session - это реальная сессия SQLAlchemy
    countries = await PlanetPolygonService.get_countries(db_session)

    # Extract country names for verification
    country_names = [country.name for country in countries]

    # Verify that we got a non-empty collection
    assert len(country_names) > 0

    # Verify that we got the expected number of countries
    assert len(countries) == 3

    # Verify that we got the expected countries
    expected_countries = ["Germany", "France", "Spain"]
    for expected in expected_countries:
        assert expected in country_names
