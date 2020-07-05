from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class WeatherResult:
    min_temp: float
    max_temp: float
    avg_temp: float
    med_temp: float


class WeatherABC(ABC):
    @abstractmethod
    def query(self, city, period) -> WeatherResult:
        pass
