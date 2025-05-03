# MCP Propertium Server

RestAPI + MCP server for OSM and Propertium data.

## Features

- OpenAI integration for text processing and PDF analysis
- SQLAlchemy + Pydantic for database models and validation
- PostgreSQL with PostGIS for spatial data storage
- Planet Polygons API for geographic data

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.12+

### Installation

1. Clone the repository
2. Run with Docker Compose:

```bash
docker-compose up -d
```

### Development Setup

```bash
# Install dependencies
uv sync
source .venv/bin/activate


uv run fastapi dev --app propertium.main:app ./src/propertium/main.py



```

## API Endpoints

### Planet Polygons

- `GET /planet-polygons/` - Get all planet polygons (paginated)
- `GET /planet-polygons/{osm_id}` - Get a specific planet polygon by OSM ID
- `POST /planet-polygons/` - Create a new planet polygon

### OpenAI Processing

- `POST /openai/pdf-to-text` - Convert PDF to text using OpenAI
- `POST /openai/text` - Process text with OpenAI

## Database Schema

The application uses SQLAlchemy with PostgreSQL and PostGIS for spatial data. The main table is `fct_planet_polygons` which stores geographic polygon data with the following fields:

- `osm_id` - Primary key, OSM ID
- `admin_level` - Administrative level
- `boundary` - Boundary type
- `name` - Name of the polygon
- `z_order` - Z-order for rendering
- `way_area` - Area of the polygon
- `way` - Geometry data (PostGIS)
- `tags` - JSON map of tags
- `country` - Country code
- `avr_rent_price` - Average rent price
- `avr_rent_price_per_m` - Average rent price per square meter
- `avr_sale_price` - Average sale price
- `avr_sale_price_per_m` - Average sale price per square meter
- `is_city_for_search` - Flag for search functionality
- `name_en` - English name
- `code` - Code
- `alpha2` - Alpha-2 code
- `border_type` - Border type

## Example Requests

### Create a Planet Polygon

```bash
curl -X POST \
  http://localhost:8000/planet-polygons/ \
  -H "Content-Type: application/json" \
  -d '{
    "osm_id": 123456789,
    "admin_level": "8",
    "boundary": "administrative",
    "name": "Example City",
    "z_order": 0,
    "way_area": 1234.56,
    "tags": {"place": "city", "population": "100000"},
    "country": "US"
  }'
```
