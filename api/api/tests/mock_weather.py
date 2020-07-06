from weather.weather import WeatherABC, WeatherResult, Period
from datetime import date


class MockWeather(WeatherABC):
    def query(self, city: str, period_start: date, period_end: date):
        return WeatherResult(
            min_temp=1,
            max_temp=30,
            avg_temp=15,
            med_temp=15,
            min_humidity=3,
            max_humidity=7,
            avg_humidity=4,
            med_humidity=4.5,
        )
