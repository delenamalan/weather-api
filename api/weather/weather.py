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

    def to_dict(self):
        return {
            "min_temp": self.min_temp,
            "max_temp": self.max_temp,
            "avg_temp": self.avg_temp,
            "med_temp": self.med_temp,
            "min_humidity": self.min_humidity,
            "max_humidity": self.max_humidity,
            "avg_humidity": self.avg_humidity,
            "med_humidity": self.med_humidity,
        }


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
