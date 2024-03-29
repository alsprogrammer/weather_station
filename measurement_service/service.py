from datetime import datetime
from typing import Union, List

from measurement_service.storages.storage_abc import MeasurementStorage
from measurement_service.models import Measurement
from utils.time_utils import get_current_timestamp


class MeasurementService:
    def __init__(self, storage: MeasurementStorage, measurement_class):
        self._storage = storage
        self._measurement_class = measurement_class

    def create_measurement(self, value: Union[int, float], timestamp: int = None) -> Measurement:
        new_measurement = self._measurement_class(value, timestamp)
        self._storage.put_measurement(new_measurement)

        return new_measurement

    def get_last_n_measurements(self, n: int) -> List[Measurement]:
        return self._storage.get_last_n_measurements(n)

    def get_measurements_between(self, from_date: datetime, to_date: datetime) -> List[Measurement]:
        return self._storage.get_measurements_between(from_date, to_date)


if __name__ == "__main__":
    from measurement_service.storages.sqlite_cursor import get_sqlite_cursor
    db_cursor = get_sqlite_cursor(':memory:')
    db_cursor.execute('CREATE TABLE Pressure (timestamp INT, value INT);')

    from measurement_service.storages.SQLMeasurementStorage import SQLMeasurementStorage
    from measurement_service.models import Measurement, PressureMeasurement, Measurement, Measurement, Measurement

    pressure_storage = SQLMeasurementStorage(db_cursor, 'Pressure', PressureMeasurement)
    pressure_service = MeasurementService(pressure_storage, PressureMeasurement)

    pressure_service.create_measurement(735, get_current_timestamp())

    measurements = pressure_service.get_last_n_measurements(10)

    print(measurements)
