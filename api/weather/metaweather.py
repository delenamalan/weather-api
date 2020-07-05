from dataclasses import dataclass
from datetime import date, timedelta
from urllib.parse import urljoin

from requests import Session

from .weather import WeatherABC, WeatherResult

BASE_URL = "https://www.metaweather.com/api/"
LOCATION_SEARCH_PATH = "location/search/"
LOCATION_PATH = "location/"


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
        url = urljoin(BASE_URL, LOCATION_SEARCH_PATH)
        response = self.session.get(url, params={"query": city})
        response.raise_for_status()
        data = response.json()
        if len(data) < 1:
            # TODO: raise error
            pass
        elif len(data) == 1:
            return data[0]["woeid"]
        else:
            # TODO: raise error or return options
            pass

    def get_weather_for_period(self, woeid: Woeid, period: Period) -> WeatherResult:
        """
        Get weather for a period. Includes start and end date.
        """
        pass

    def get_weather_for_day(self, woeid: Woeid, day: date):
        """
        Get the weather for a given day.
        """
        day_str = day.strftime("%Y/%m/%d")
        url = urljoin(BASE_URL, f"{LOCATION_PATH}/{woeid}/{day_str}")
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()
        return data
        # if len(data) < 1:
        #     # TODO: raise error
        #     pass
        # elif len(data) == 1:
        #     return data[0]['woeid']
        # else:
        #     # TODO: raise error or return options
        #     pass
