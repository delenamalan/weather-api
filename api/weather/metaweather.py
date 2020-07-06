from dataclasses import dataclass
from datetime import date, timedelta
from urllib.parse import urljoin
from statistics import mean, median
import logging

from requests import Session

from weather.weather import WeatherABC, WeatherResult, Period

BASE_URL = "https://www.metaweather.com/api/"
LOCATION_SEARCH_URL = f"{BASE_URL}location/search/"
LOCATION_URL = f"{BASE_URL}location/"

logger = logging.getLogger(__name__)


class NoWeatherForDayFoundException(Exception):
    def __init__(self, msg="No weather found for day.", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class NoManyWoeidFound(Exception):
    def __init__(self, msg="City not found.", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class TooManyWoeidsFound(Exception):
    def __init__(
        self,
        msg="Too many cities match this query. Please try a more specific name.",
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)


@dataclass
class MetaWeatherForDayResult:
    min_temp: float
    max_temp: float
    humidity: float


class Woeid(int):
    """
    Class to represent a "Where On Earth ID."
    """

    pass


class MetaWeather(WeatherABC):
    def __init__(self):
        self.api = MetaWeatherApi()

    def query(self, city: str, period_start: date, period_end: date):
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
        logger.info(f"Getting woeid for '{city}'.")
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
        Get weather statistics for a period. Includes start and end date.
        """
        min_temps = []
        max_temps = []
        avg_temps = []
        humidities = []
        for day in period.days:
            day_weather = self.get_weather_for_day(woeid, day)

            # MetaWeather doesn't return an average temperature for a day or for any
            # other range. It only returns a min and max temperature. So we calculate
            # a "mean" below using the min and max temperature for a day which is
            # obviously not correct, but the closest we can get with the given data.
            avg_temp = mean((day_weather.min_temp, day_weather.max_temp))

            min_temps.append(day_weather.min_temp)
            max_temps.append(day_weather.max_temp)
            avg_temps.append(avg_temp)
            humidities.append(day_weather.humidity)

        return WeatherResult(
            min_temp=min(min_temps),
            max_temp=max(max_temps),
            avg_temp=mean(avg_temps),
            med_temp=median(avg_temps),
            min_humidity=min(humidities),
            max_humidity=max(humidities),
            avg_humidity=mean(humidities),
            med_humidity=median(humidities),
        )

    def get_weather_for_day(self, woeid: Woeid, day: date) -> MetaWeatherForDayResult:
        """
        Get the weather for a given day.
        """
        logger.info(f"Getting weather for {day} for woeid {woeid}.")
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
