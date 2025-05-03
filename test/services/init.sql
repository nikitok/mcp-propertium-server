-- Initialize test data for PlanetPolygonService tests
-- Create the table if it doesn't exist
CREATE TABLE IF NOT EXISTS fct_planet_polygons (
    osm_id BIGINT PRIMARY KEY,
    admin_level TEXT,
    boundary TEXT,
    name TEXT,
    z_order INTEGER,
    way_area FLOAT,
    country TEXT,
    avr_rent_price FLOAT,
    avr_rent_price_per_m FLOAT,
    avr_sale_price FLOAT,
    avr_sale_price_per_m FLOAT,
    is_city_for_search BOOLEAN,
    name_en TEXT,
    code TEXT,
    alpha2 TEXT,
    border_type TEXT
);

-- Clear existing data
DELETE FROM fct_planet_polygons;

-- Insert test countries (admin_level = 2)
INSERT INTO fct_planet_polygons (
    osm_id, admin_level, boundary, name, country, name_en, alpha2
) VALUES 
(1, '2', 'administrative', 'Germany', 'DE', 'Germany', 'DE'),
(2, '2', 'administrative', 'France', 'FR', 'France', 'FR'),
(3, '2', 'administrative', 'Spain', 'ES', 'Spain', 'ES');

-- Insert test cities (admin_level = 4)
INSERT INTO fct_planet_polygons (
    osm_id, admin_level, boundary, name, country, name_en
) VALUES 
(101, '4', 'administrative', 'Berlin', 'DE', 'Berlin'),
(102, '4', 'administrative', 'Paris', 'FR', 'Paris'),
(103, '4', 'administrative', 'Madrid', 'ES', 'Madrid');