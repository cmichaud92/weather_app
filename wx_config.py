from collections import namedtuple

Coordinates = namedtuple(
    'Coordinates',
    'latitude, longitude'
    )

BASE_URL = "https://api.weather.gov"

forecast_locations = {
    'death valley': {
        'coordinates': {
            'latitude': 36.45699,
            'longitude': -116.86393,
        },
        'elevation': -287
    },
    'castle valley': {
        'coordinates': {
            'latitude': 38.6487,
            'longitude': -109.42783,
        },
        'elevation': 4600
    },
    'fishlake': {
        'coordinates': {
            'latitude': 38.81719,
            'longitude': -111.53427,
        },
        'elevation': 7000
    },
    'soldiers summit': {
        'coordinates': {
            'latitude': 39.92366,
            'longitude': -111.06842,
        },
        'elevation': 7400
    },
    'phantom ranch': {
        'coordinates': {
            'latitude': 36.09933,
            'longitude': -112.09297,
        },
        'elevation': 2458
    },
    'lees ferry': {
        'coordinates': {
            'latitude': 36.86595,
            'longitude': -111.5871,
        },
        'elevation': 3129
    },
}
