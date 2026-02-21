
import pytest
import requests

from wx_config import (
    Coordinates,
)
from wx_utils import (
    generate_location_url,
    # get_user_location,
    get_coordinates,
    get_forecast_url,
    make_api_call,
    parse_forecast_response,
    print_forecast,
    safe_api_call,
)

# ===== get_coordinates() tests =====

@pytest.mark.parametrize("location, expected", [
    ('death valley', Coordinates(36.45699, -116.86393)),
    ('castle valley', Coordinates(38.6487, -109.42783)),
    ('fishlake', Coordinates(38.81719, -111.53427))
])
def test_get_coordinates_valid_locations(location, expected):
    # Arrange - decorator above
    # Act & Assert
    assert get_coordinates(location) == expected


def test_get_coordinates_invalid_location():
    # Arrange
    with pytest.raises(ValueError) as exc_info:
        # Act
        get_coordinates('nowhere')
    # Assert and check error message (optional)
    assert "Unknown location: nowhere" in str(exc_info)


def test_get_coordinates_with_whitespace():
    # Arrange
    location = ' death valley'
    expected = Coordinates(36.45699, -116.86393)

    # Act
    result = get_coordinates(location)

    # Assert
    assert result == expected


def test_get_coordinates_with_mixed_case():
    # Arrange
    location = 'DEATH VALley'

    expected = Coordinates(36.45699, -116.86393)

    # Act
    result = get_coordinates(location)

    # Assert
    assert result == expected


# ===== generate_location_url() tests =====

def test_generate_location_url_default_base():
    # Arrange
    lat = 36.45699
    lon = -116.86393

    # Act
    result = generate_location_url(lat, lon)

    # Assert
    assert result == "https://api.weather.gov/points/36.45699,-116.86393"


def test_generate_location_url_custom_base():
    # Arrange
    lat = 36.45699
    lon = -116.86393
    base_url = "https://google.com"

    # Act
    result = generate_location_url(lat, lon, base_url)

    # Assert
    assert result == "https://google.com/points/36.45699,-116.86393"


# ===== get_forecast_url() tests =====

def test_get_forecast_url_valid_response():
    # Arrange
    mock_response = {
        'properties': {
            'forecast': 'https://api.weather.gov/gridpoints/VEF/63,120/forecast'
        }
    }

    # Act
    result = get_forecast_url(mock_response)

    # Assert
    assert result == 'https://api.weather.gov/gridpoints/VEF/63,120/forecast'


@pytest.mark.parametrize("invalid_response", [
    {},                                 # Empty dict
    None,                               # None input
    {'properties': {}},                 # Missing forecast key
    {'wrong_key': 'value'}              # Wrong structure
])
def test_get_forecast_url_invalid_response(invalid_response):
    # Act
    result = get_forecast_url(invalid_response)

    # Assert
    assert result is None


# ===== parse_forecast_response() tests =====

def test_parse_valid_forecast_response():
    location = 'lees ferry'
    mock_response = {
        'properties': {
            'periods': [
                {
                    'name': 'This Afternoon',
                    'detailedForecast': 'Snow, snow, snow'
                },
                {
                    'name': 'Tonight',
                    'detailedForecast': 'Rain :)'
                },
            ]
        }
    }

    result = parse_forecast_response(mock_response, location)

    assert result == {
        'lees ferry': [
            {'name': 'This Afternoon', 'detailedForecast': 'Snow, snow, snow'},
            {'name': 'Tonight', 'detailedForecast': 'Rain :)'},
        ]
    }


@pytest.mark.parametrize("invalid_response", [
    {},                                 # Empty dict
    None,                               # None input
    {'properties': {}},                 # Missing properties
    # {'properties': {'periods': []}},    # Missing periods
    {'wrong_key': 'value'}              # Wrong structure
])
def test_parse_invalid_forecast_response(invalid_response):

    result = parse_forecast_response(invalid_response, 'test_location')

    assert result is None


# ===== make_api_call() tests =====

def test_make_api_call_success(mocker):
    # Arrange
    mock_response = mocker.Mock()
    mock_response.json.return_value = {'properties': {'forecast': 'url'}}

    # Mock requests.get to return our moch response
    mocker.patch('wx_utils.requests.get', return_value=mock_response)

    # Act - call the function
    result = make_api_call('http://test.com')

    # Assert - check the return value is correct
    assert result == {'properties': {'forecast': 'url'}}


def test_make_api_call_http_error(mocker):
    # Arrange
    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "404 Not Found"
    )

    mocker.patch('wx_utils.requests.get', return_value=mock_response)

    # Act & Assert
    with pytest.raises(requests.exceptions.HTTPError):
        make_api_call('http://test.com')


def test_make_api_call_connection_error(mocker):
    # Arrange
    mocker.patch(
        'wx_utils.requests.get',
        side_effect=requests.exceptions.ConnectionError("Network down")
    )

    # Act & Assert
    with pytest.raises(requests.exceptions.ConnectionError):
        make_api_call('http://tests.com')


def test_make_api_call_timeout(mocker):
    # Arrange
    mocker.patch(
        'wx_utils.requests.get',
        side_effect=requests.exceptions.Timeout("Request timeout")
    )

    # Act & Assert
    with pytest.raises(requests.exceptions.Timeout):
        make_api_call('http://tests.com')


# ===== safe_api_call() tests =====

def test_safe_api_call_success(mocker):
    # Mock make_api_call() to return valid data
    mocker.patch('wx_utils.make_api_call', return_value={'data': 'value'})

    result = safe_api_call('http://test.com')

    assert result == {'data': 'value'}


@pytest.mark.parametrize("exception", [
    requests.exceptions.HTTPError("404"),
    requests.exceptions.ConnectionError("Network down"),
    requests.exceptions.Timeout("Timeout"),
    Exception("Unexpected error")
])
def test_safe_api_call_errors(mocker, exception):
    mocker.patch('wx_utils.make_api_call', side_effect=exception)

    result = safe_api_call('http://test.com')

    assert result is None


# ===== print_forecast() tests =====

def test_print_forecast_does_not_crash():
    forecast_data = {
        'death valley': [
            {'name': 'Tonight', 'detailedForecast': 'Clear skies'}
        ]
    }
    # Verify it does not raise an exception
    print_forecast(forecast_data)
