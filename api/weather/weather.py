from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class WeatherResult:
    min_temp: float
    max_temp: float
    avg_temp: float
    med_temp: float
    min_humidity: float
    max_humidity: float
    avg_humidity: float
    med_humidity: float


class WeatherABC(ABC):
    @abstractmethod
    def query(self, city, period) -> WeatherResult:
        pass


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
