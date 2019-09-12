# pylint: skip-file

"""Testing module api_dwdweather"""
import unittest

from weatherstation.api import dwdweather


class TestApiDwdWeather(unittest.TestCase):

    def test_download_webpage(self):
        result = dwdweather.download_webpage()

        self.assertIsNotNone(result)
        self.assertIn("<!DOCTYPE html>", str(result))


    def test_scrap_weather_nodes_from_html(self):
        test_data = bytes('<div id="wettertext"><h3>foo</h3><h2>bar</h2></div>', 'utf-8')

        result = dwdweather.scrap_weather_nodes_from_html(test_data)

        self.assertCountEqual(["foo", "bar"], result)


    def test_cleanup_scrapped_weather_data(self):
        test_data = [
            'WARNLAGEBERICHT für Deutschland',
            'ausgegeben vom Deutschen Wetterdienst',
            'Entwicklung der WETTER- und WARNLAGE für die nächsten 24 Stunden',
            '',
            '\r',
            '\n',
            '   ',
            'FROST: In der Südhälfte nachts leichter Frost zwischen 0 und -5 Grad. Örtlich darunter.',
            'Nächste Aktualisierung: spätestens Mittwoch, 15.11.2017, 16:00 Uhr'
        ]

        result = dwdweather.cleanup_scrapped_weather_data(test_data)

        self.assertNotIn("", result)


    def test_download_dwd_weather_data(self):
        result = dwdweather.download_dwd_weather_data()

        self.assertTrue(len(result) > 0)

if __name__ == "__main__":
    unittest.main()
