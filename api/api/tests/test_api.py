from django.test import TestCase, Client, override_settings
from django.urls import reverse


@override_settings(WEATHER_CLASS="api.tests.mock_weather.MockWeather")
class WeatherApiTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_weather(self):
        response = self.client.get(
            reverse("api.weather"),
            {"city": "test city", "period": "2020/01/02-2020/01/04"},
        )
        self.assertEqual(200, response.status_code)
        result = response.json()
        self.assertEqual(
            {
                "min_temp": 1,
                "max_temp": 30,
                "avg_temp": 15,
                "med_temp": 15,
                "min_humidity": 3,
                "max_humidity": 7,
                "avg_humidity": 4,
                "med_humidity": 4.5,
            },
            result,
        )
