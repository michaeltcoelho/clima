from typing import NamedTuple


class WeatherMetric(NamedTuple):
    city: str
    state: str
    month: str
    min_temp: int
    max_temp: int
    rain: int
