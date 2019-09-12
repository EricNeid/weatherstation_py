# pylint: skip-file

"""Testing module api_openweather"""
import unittest
import os

from weatherstation.api import openweather


class TestApiOpenWeather(unittest.TestCase):
    real_key = os.path.abspath("./weatherstation/resources/api.key")

    def test_download_weather_data(self):
        """
        should download current weather data for city london
        - needs a working api key in module
        - just check for exception
        """
        key = self.__get_real_api_key()

        result = openweather.download_weather_data("London", key)

        self.assertIsNotNone(result)


    def __get_real_api_key(self):
        with open(self.real_key, "r") as f:
            return f.readline().strip()


if __name__ == "__main__":
    unittest.main()
