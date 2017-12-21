"""
Model classes for weather information
"""

import jsonpickle
import utils

class WeatherDataDaily:
    """
    Container for weather data of a single day
    Containing temperature and weather condition
    """
    time_unix = ""
    temperature_day = ""
    temperature_min = ""
    temperature_max = ""
    condition_id = ""
    condition_icon = ""

    def update_from_json(self, json_forecast_day):
        """
        Updates weather data by parsing given json
        Returns self
        """
        self.time_unix = str(json_forecast_day["dt"])
        self.temperature_day = str(json_forecast_day["temp"]["day"])
        self.temperature_min = str(json_forecast_day["temp"]["min"])
        self.temperature_max = str(json_forecast_day["temp"]["max"])
        self.condition_id = str(json_forecast_day["weather"][0]["id"])
        self.condition_icon = str(json_forecast_day["weather"][0]["icon"])
        return self


    def __eq__(self, other):
        if self.time_unix == other.time_unix and \
            self.temperature_day == other.temperature_day and \
            self.temperature_min == other.temperature_min and \
            self.temperature_max == other.temperature_max and \
            self.condition_id == other.condition_id and \
            self.condition_icon == other.condition_icon:
            return True
        return False


    def __ne__(self, other):
        return not self.__eq__(other)


class WeatherData:
    """
    Container for weather data forecast.
    It contains the  current temperature and a forecast of the next 3 days.

    Raises ParseWeatherDataException if the supplied json is not in the expected structure.
    """
    timestamp = ""
    current_temperature = ""
    forecast = []

    def __init__(self, json_temperature, json_forecast):
        self.timestamp = utils.get_time_human_readable()

        try:
            self.current_temperature = str(json_temperature["main"]["temp"])
        except KeyError as error:
            raise ParseWeatherDataException(
                "Temperature data is not as expected: " + str(error) + "\n" +
                "Received: " + json_temperature
            )

        try:
            self.forecast = [
                WeatherDataDaily().update_from_json(json_forecast["list"][day])
                for day in range(0, 3)
            ]
        except KeyError as error:
            raise ParseWeatherDataException(
                "Forecast data is not as expected: " + str(error) + "\n" +
                "Received: " + json_forecast
            )


def write_to_file(weather_data, file_name):
    """
    Serialize this object to file
    """
    text = jsonpickle.encode(weather_data)
    with open(file_name, "w") as file:
        file.write(text)


def read_from_file(file_name):
    """
    Serialize this object to file
    """
    text = ""
    with open(file_name, "r") as file:
        text = file.read()
    return jsonpickle.decode(text)


class ParseWeatherDataException(Exception):
    """
    ParseWeatherDataException is raised if the downloaded weather data could
    not be parsed into the model. This usually happens when the server answers
    in an unexpected fashion.
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
