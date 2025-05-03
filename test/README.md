# Tests for MCP Propertium Server

This directory contains tests for the MCP Propertium Server project.

## Running Tests

To run the tests, you need to have pytest installed. If you haven't installed it yet, you can do so by running:

```bash
pip install -e ".[dev]"
```

This will install the project in development mode with all the development dependencies, including pytest.

### Running all tests

To run all tests, execute the following command from the project root:

```bash
pytest
```

### Running specific tests

To run a specific test file:

```bash
pytest test/test_planet_polygon.py
```

To run a specific test function:

```bash
pytest test/test_planet_polygon.py::test_create_polygon
```

## Test Structure

The tests are organized as follows:

- `test_planet_polygon.py`: Tests for the Planet Polygon API endpoints