# pylint: skip-file

"""Testing module api_dwdweather"""
import unittest
import aiounittest
import asyncio

import context
import api_dwdweather


class TestApiDwdWeather(aiounittest.AsyncTestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()


    async def test_download_webpage(self):
        result = await api_dwdweather.download_webpage()

        self.assertIsNotNone(result)
        self.assertIn("<!DOCTYPE html>", str(result))


    async def test_scrap_weather_nodes_from_html(self):
        test_data = bytes('<div id="wettertext"><h3>foo</h3><h2>bar</h2></div>', 'utf-8')

        result = await api_dwdweather.scrap_weather_nodes_from_html(test_data)

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

        result = api_dwdweather.cleanup_scrapped_weather_data(test_data)

        self.assertNotIn("", result)


    async def test_download_dwd_weather_data(self):
        result = await api_dwdweather.download_dwd_weather_data()

        self.assertTrue(len(result) > 0)

if __name__ == "__main__":
    unittest.main()
