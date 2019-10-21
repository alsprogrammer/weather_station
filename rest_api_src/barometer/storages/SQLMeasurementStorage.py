from datetime import datetime

from rest_api_src.barometer.models import Measurement
from rest_api_src.barometer.storages.storage_abc import MeasurementStorage


class SQLMeasurementStorage(MeasurementStorage):
    def __init__(self, dbcursor, table_name: str, measurement_type):
        self._dbcursor = dbcursor
        self._table_name = table_name

        self._put_measurement_query = 'INSERT INTO {table_name} VALUES (?, ?)'.format(table_name=self._table_name)
        self._get_last_n_measurements_query = 'SELECT timestamp, value FROM {table_name}' \
                                              ' ORDER BY timestamp DESC LIMIT ?'\
            .format(table_name=self._table_name)
        self._get_measurements_between_query = 'SELECT timestamp, value FROM {table_name} ' \
                                               'WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp DESC'\
            .format(table_name=self._table_name)

        self._measurement_type = measurement_type

    def put_measurement(self, measurement: Measurement):
        self._dbcursor.execute(self._put_measurement_query, (measurement.timestamp, measurement.value))

    def get_last_n_measurements(self, n: int):
        row_set = self._dbcursor.execute(self._get_last_n_measurements_query, (n,))
        measurements = self._get_measurements_from_rowset(row_set)

        return measurements[::-1]

    def _get_measurements_from_rowset(self, row_set):
        measurements = []
        for row in row_set:
            measurements.append(self._measurement_type(row[1], row[0]))
        return measurements

    def get_measurements_between(self, from_date: datetime, to_date: datetime):
        row_set = self._dbcursor.execute(self._get_measurements_between_query, (from_date, to_date))
        measurements = self._get_measurements_from_rowset(row_set)

        return measurements[::-1]


if __name__ == "__main__":
    import sqlite3
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()

    c.execute('CREATE TABLE Pressure (timestamp INT, value INT);')

    from barometer.models import PressureMeasurement
    storage = SQLMeasurementStorage(c, 'Pressure', PressureMeasurement)

    cur_measurement = PressureMeasurement(735)

    storage.put_measurement(cur_measurement)

    from time import sleep
    sleep(0.1)

    new_measurement = PressureMeasurement(745)

    storage.put_measurement(new_measurement)

    measurements = storage.get_last_n_measurements(10)
    print(measurements)
