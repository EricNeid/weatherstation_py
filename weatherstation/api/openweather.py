"""
Get wether data from OpenWetherMap
http://openweathermap.org/help/city_list.txt
"""
import requests

from weatherstation.api import weatherdata


API_ENDPOINT_TEMPERATURE = "http://api.openweathermap.org/data/2.5/weather"
API_ENDPOINT_FORECAST = "http://api.openweathermap.org/data/2.5/forecast/daily"
API_ENDPOINT_WEATHER_ICON = "http://openweathermap.org/img/w"


def get_temperature_json(city, api_key):
    """Call OpenWeatherMap api to get temperature data"""
    request = API_ENDPOINT_TEMPERATURE + "?" + __get_url_params(city, api_key)
    response = requests.get(request)
    return response.json()


def get_forecast_json(city, api_key):
    """Call OpenWeatherMap api to get daily forecast"""
    request = API_ENDPOINT_FORECAST + "?" + __get_url_params(city, api_key)
    response = requests.get(request)
    return response.json()


def download_weather_data(city, api_key):
    """Returns WeatherData, downloaded from OpenWeatherMap"""
    try:
        temperature_json = get_temperature_json(city, api_key)
    except requests.exceptions.RequestException as error:
        raise RetrieveWeatherDataException(
            "Could not download data for current temperature, cause of: " + str(error)
        )

    try:
        forecast_json = get_forecast_json(city, api_key)
    except requests.exceptions.RequestException as error:
        raise RetrieveWeatherDataException(
            "Could not download forecast data, cause of: " + str(error)
        )

    return weatherdata.WeatherData(temperature_json, forecast_json)


def get_url_for_weather(weather_icon):
    """Return url pointing to icon suitable for given weather"""
    return "{}/{}.png".format(API_ENDPOINT_WEATHER_ICON, weather_icon)


def __get_url_params(city, api_key):
    return "q={}&appid={}&units=metric".format(city, api_key)


class RetrieveWeatherDataException(Exception):
    """
    RetrieveWeatherDataException is raised if the download of weather data fails.
    This is usually the case if an connection error occurs or in case of a timeout.
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
