import json
import os
from unittest.mock import patch
from datetime import date

import requests_mock
from django.test import TestCase
from requests import Session

from weather.metaweather import (
    MetaWeatherApi,
    Woeid,
    NoManyWoeidFound,
    TooManyWoeidsFound,
    Period,
    MetaWeatherForDayResult,
)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_json_from_file(file_name):
    with open(os.path.join(CURRENT_DIR, "data", file_name)) as f:
        return json.load(f)


class MetaWeatherApiTest(TestCase):
    def setUp(self):
        self.session = Session()
        self.adapter = requests_mock.Adapter()
        self.session.mount("https://", self.adapter)
        self.adapter.register_uri("GET", "mock://test.com", json={"hello": "world"})
        self.api = MetaWeatherApi(session=self.session)

    def test_no_woeid(self):
        self.adapter.register_uri(
            "GET",
            "https://www.metaweather.com/api/location/search/",
            json=load_json_from_file("no_woeid_result.json"),
        )
        with self.assertRaises(NoManyWoeidFound):
            result = self.api.get_woeid("asdalkjasdlkajsalksjdasdlkj")

    def test_multiple_woeids(self):
        self.adapter.register_uri(
            "GET",
            "https://www.metaweather.com/api/location/search/",
            json=load_json_from_file("multiple_woeid_result.json"),
        )
        with self.assertRaises(TooManyWoeidsFound):
            result = self.api.get_woeid("lon")

    def test_get_single_woeid(self):
        self.adapter.register_uri(
            "GET",
            "https://www.metaweather.com/api/location/search/",
            json=load_json_from_file("one_woeid_result.json"),
        )
        result = self.api.get_woeid("london")
        self.assertEqual(result, 44418)

    def test_get_weather_for_day(self):
        self.adapter.register_uri(
            "GET",
            "https://www.metaweather.com/api/location/44418/2013/04/27",
            json=load_json_from_file("hourly_weather_for_day.json"),
        )
        result = self.api.get_weather_for_day(44418, date(2013, 4, 27))
        self.assertEqual(result.min_temp, 3.07)
        self.assertEqual(result.max_temp, 10.01)
        self.assertEqual(result.humidity, 74)

    def test_get_weather_for_period(self):
        def mock_day_weathers(woeid, day):
            return MetaWeatherForDayResult(min_temp=1, max_temp=10, humidity=10,)

        period = Period(date(2013, 4, 27), date(2013, 4, 29))
        with patch.object(
            self.api, "get_weather_for_day", side_effect=mock_day_weathers
        ):
            result = self.api.get_weather_for_period(44418, period)
            self.assertEqual(result.min_temp, 1)
            self.assertEqual(result.max_temp, 10)
            self.assertEqual(result.avg_temp, 5.5)
            self.assertEqual(result.med_temp, 5.5)
            self.assertEqual(result.min_humidity, 10)
            self.assertEqual(result.max_humidity, 10)
            self.assertEqual(result.avg_humidity, 10)
            self.assertEqual(result.med_humidity, 10)
