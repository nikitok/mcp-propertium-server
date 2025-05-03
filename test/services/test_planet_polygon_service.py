import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

# Import the service directly
from src.propertium.services.planet_polygon_service import PlanetPolygonService
from src.propertium.schemas.geo_schemas import GeoPoint

@pytest.fixture
def mock_db_session():
    """Create a mock database session for testing."""
    session = AsyncMock()
    return session


@pytest.mark.asyncio
async def test_get_polygon_by_osm_id(mock_db_session):
    """Test getting a polygon by OSM ID."""
    # Create a mock polygon
    country = MagicMock()
    country.osm_id = 1
    country.name = "Test Country"
    country.admin_level = "2"

    # Set up the mock to return the country when execute is called
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = country
    mock_db_session.execute.return_value = mock_result

    # Get the country polygon
    polygon = await PlanetPolygonService.get_polygon_by_osm_id(mock_db_session, 1)

    assert polygon is not None
    assert polygon.osm_id == 1
    assert polygon.name == "Test Country"
    assert polygon.admin_level == "2"

    # Set up the mock to return None for a non-existent polygon
    mock_result.scalars.return_value.first.return_value = None

    # Get a non-existent polygon
    polygon = await PlanetPolygonService.get_polygon_by_osm_id(mock_db_session, 999)
    assert polygon is None

@pytest.mark.asyncio
async def test_get_polygons_by_location(mock_db_session):
    """Test finding polygons that contain a point."""
    # Create mock polygons
    country = MagicMock()
    country.osm_id = 1
    country.name = "Test Country"
    country.admin_level = "2"

    city = MagicMock()
    city.osm_id = 2
    city.name = "Test City"
    city.admin_level = "4"

    # Set up the mock to return both polygons for a point inside both
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [country, city]
    mock_db_session.execute.return_value = mock_result

    # Point inside both country and city
    point = GeoPoint(lat=5.0, lng=5.0)
    polygons = await PlanetPolygonService.get_polygons_by_location(mock_db_session, point)

    # Should find both country and city
    assert len(polygons) == 2
    osm_ids = [p.osm_id for p in polygons]
    assert 1 in osm_ids  # Country
    assert 2 in osm_ids  # City

    # Set up the mock to return only the country for a point inside country but outside city
    mock_result.scalars.return_value.all.return_value = [country]

    # Point inside country but outside city
    point = GeoPoint(lat=1.0, lng=1.0)
    polygons = await PlanetPolygonService.get_polygons_by_location(mock_db_session, point)

    # Should find only country
    assert len(polygons) == 1
    assert polygons[0].osm_id == 1

    # Set up the mock to return nothing for a point outside both
    mock_result.scalars.return_value.all.return_value = []

    # Point outside both
    point = GeoPoint(lat=20.0, lng=20.0)
    polygons = await PlanetPolygonService.get_polygons_by_location(mock_db_session, point)

    # Should find nothing
    assert len(polygons) == 0

@pytest.mark.asyncio
async def test_get_countries(mock_db_session):
    """Test getting all countries using mock."""
    # Create a mock country
    country = MagicMock()
    country.osm_id = 1
    country.name = "Test Country"
    country.admin_level = "2"

    # Set up the mock to return the country when execute is called
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [country]
    mock_db_session.execute.return_value = mock_result

    # Get all countries
    countries = await PlanetPolygonService.get_countries(mock_db_session)

    assert len(countries) == 1
    assert countries[0].osm_id == 1
    assert countries[0].name == "Test Country"
    assert countries[0].admin_level == "2"
