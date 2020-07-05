from dataclasses import dataclass
from datetime import date, timedelta
from urllib.parse import urljoin

from requests import Session

from .weather import WeatherABC, WeatherResult

BASE_URL = "https://www.metaweather.com/api/"
LOCATION_SEARCH_URL = f"{BASE_URL}location/search/"
LOCATION_URL = f"{BASE_URL}location/"


class NoWeatherForDayFoundException(Exception):
    pass


class NoManyWoeidFound(Exception):
    pass


class TooManyWoeidsFound(Exception):
    pass


@dataclass
class MetaWeatherForDayResult:
    min_temp: float
    max_temp: float
    humidity: float


@dataclass
class Period:
    start_date: date
    end_date: date

    @property
    def days(self):
        days = []
        current_date = self.start_date
        while current_date <= self.end_date:
            days.append(current_date)
            current_date += timedelta(days=1)
        return days


class Woeid(int):
    pass


class MetaWeather(WeatherABC):
    def __init__(self):
        self.api = MetaWeatherApi()

    def query(self, city, period_start, period_end):
        woeid = self.api.get_woeid(city)
        period = Period(period_start, period_end)
        return self.api.get_weather_for_period(woeid, period)


class MetaWeatherApi:
    def __init__(self, session=None):
        if session is None:
            self.session = Session()
        else:
            self.session = session

    def get_woeid(self, city: str) -> Woeid:
        """ Get the Where on Earth identifier for a city"""
        response = self.session.get(LOCATION_SEARCH_URL, params={"query": city})
        response.raise_for_status()
        data = response.json()
        if len(data) < 1:
            raise NoManyWoeidFound()
        elif len(data) == 1:
            return data[0]["woeid"]
        else:
            raise TooManyWoeidsFound()

    def get_weather_for_period(self, woeid: Woeid, period: Period) -> WeatherResult:
        """
        Get weather for a period. Includes start and end date.
        """
        pass

    def get_weather_for_day(self, woeid: Woeid, day: date) -> MetaWeatherForDayResult:
        """
        Get the weather for a given day.
        """
        day_str = day.strftime("%Y/%m/%d")
        url = f"{LOCATION_URL}{woeid}/{day_str}"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()
        if len(data) < 1:
            raise NoWeatherForDayFoundException()

        # Metaweather returns data from multiple sources for the same day so
        # we have to select one of them
        chosen_result = data[0]
        return MetaWeatherForDayResult(
            min_temp=chosen_result["min_temp"],
            max_temp=chosen_result["max_temp"],
            humidity=chosen_result["humidity"],
        )
