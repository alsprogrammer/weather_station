from abc import ABC, abstractmethod
from datetime import datetime


from rest_api_src.barometer.models import Measurement


class MeasurementStorage(ABC):
    @abstractmethod
    def put_measurement(self, measurement: Measurement):
        raise NotImplementedError()

    @abstractmethod
    def get_last_n_measurements(self, n: int):
        raise NotImplementedError()

    @abstractmethod
    def get_measurements_between(self, from_date: datetime, to_date: datetime):
        raise NotImplementedError()
