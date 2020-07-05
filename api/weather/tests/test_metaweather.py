from django.test import TestCase
from unittest.mock import MagicMock
from weather.metaweather import MetaWeatherApi
import json
import os
from requests import Session
import requests_mock

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_json_from_file(file_name):
    with open(os.path.join(CURRENT_DIR, "data", file_name)) as f:
        return json.load(f)


class MetaWeatherApiTest(TestCase):
    def setUp(self):
        session = Session()
        adapter = requests_mock.Adapter()
        session.mount("mock://", adapter)
        adapter.register_uri(
            "GET",
            "https://www.metaweather.com/api/location/search/",
            json=load_json_from_file("one_woeid_result.json"),
        )
        self.api = MetaWeatherApi(session=session)

    def test_get_woeid(self):
        result = self.api.get_woeid("london")
        self.assertEqual(result, 44418)
