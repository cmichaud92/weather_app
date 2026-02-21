# Weather API

A Python command-line application that retrieves weather forecasts from the National Weather Service (NWS) API for predefined locations across the American Southwest.

## Overview

This application provides an easy-to-use interface for fetching detailed weather forecasts for specific locations. It interacts with the NWS API to retrieve up-to-date forecast information based on geographic coordinates.

## Features

- **CLI and Interactive Modes**: Run with location argument or use interactive prompts
- **Predefined Locations**: Six scenic locations pre-configured with coordinates and elevations:
  - Death Valley, CA (-287 ft)
  - Castle Valley, UT (4,600 ft)
  - Fishlake, UT (7,000 ft)
  - Soldiers Summit, UT (7,400 ft)
  - Phantom Ranch, AZ (2,458 ft)
  - Lees Ferry, AZ (3,129 ft)
- **Error Handling**: Robust exception handling for network issues and API errors
- **Comprehensive Testing**: Full pytest test suite with parametrized tests

## Installation

```bash
# Install dependencies
uv sync
```

## Usage

**Command-line mode:**
```bash
python weather_api.py "death valley"
```

**Interactive mode:**
```bash
python weather_api.py
# Then select from the available locations when prompted
```

## Project Structure

- `weather_api.py` - Main entry point with CLI argument parsing
- `wx_config.py` - Configuration file containing location coordinates and base API URL
- `wx_utils.py` - Utility functions for API calls, data parsing, and output formatting
- `test_weather_api.py` - Pytest test suite with comprehensive unit tests
- `pyproject.toml` - Project configuration and dependencies

## Testing

Run the test suite:
```bash
pytest test_weather_api.py -v
```

## API

This application uses the [National Weather Service API](https://www.weather.gov/documentation/services-web-api), which provides free access to weather forecasts for locations within the United States.

## Development

- Python 3.12+
- Linting: Ruff (configured for 100 character line length)
- Testing: pytest
