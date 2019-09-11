# pylint: skip-file

"""Testing module gui_weatherstation"""
import unittest
import os

os.environ["KIVY_NO_CONSOLELOG"] = "1" # disable kivy logger

from weatherstation import gui_weatherstation


class TestGuiWeatherStation(unittest.TestCase):
    test_data_dir = os.path.abspath("./tests/test_data_gui_weatherstation")
    test_key = os.path.join(test_data_dir, "key.txt")

    def test_read_api_key(self):
        """should return content of api key file"""
        key = gui_weatherstation.read_api_key(self.test_key)

        self.assertEqual("1234567890", key)

if __name__ == "__main__":
    unittest.main()
