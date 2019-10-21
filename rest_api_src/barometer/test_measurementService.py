from unittest import TestCase

from rest_api_src.barometer.service import MeasurementService
from rest_api_src.barometer.storages.sqlite_cursor import get_sqlite_cursor
from rest_api_src.barometer.storages.SQLMeasurementStorage import SQLMeasurementStorage
from rest_api_src.barometer.models import PressureMeasurement
from rest_api_src.barometer.utils.time_utils import get_current_timestamp


class TestMeasurementService(TestCase):
    def setUp(self) -> None:
        self._old_time_stamp = 946684800000  # 2000-01-01 00:00:00
        self.db_cursor = get_sqlite_cursor(':memory:')
        self.db_cursor.execute('CREATE TABLE Pressure (timestamp INT, value INT);')
        self.db_cursor.execute('INSERT INTO Pressure VALUES (?, ?);', (self._old_time_stamp, 735,))

        self.pressure_storage = SQLMeasurementStorage(self.db_cursor, 'Pressure', PressureMeasurement)
        self.pressure_service = MeasurementService(self.pressure_storage, PressureMeasurement)

    def test_create_measurement(self):
        count_query = 'SELECT Count(*) FROM Pressure;'
        measurements_num = self.db_cursor.execute(count_query).fetchone()[0]
        timestamp = get_current_timestamp()
        self.pressure_service.create_measurement(600, timestamp)
        measurements_num_after = self.db_cursor.execute(count_query).fetchone()[0]
        self.assertEqual(measurements_num + 1, measurements_num_after)
        created_measurements_num = self.db_cursor.execute('SELECT Count(*) FROM Pressure WHERE timestamp=?;',
                                                          (timestamp,)).fetchone()[0]
        self.assertEqual(created_measurements_num, 1)

    def test_last_n_measurements(self):
        count_query = 'SELECT Count(*) FROM Pressure;'
        measurements_num = self.db_cursor.execute(count_query).fetchone()[0]
        measurements_list = self.pressure_service.get_last_n_measurements(1)
        self.assertEqual(len(measurements_list), measurements_num)
        current_timestamp = get_current_timestamp()
        self.db_cursor.execute('INSERT INTO Pressure VALUES (?, ?);', (current_timestamp, 735,))
        measurements_list = self.pressure_service.get_last_n_measurements(1)
        self.assertEqual(len(measurements_list), 1)
        measurements_list = self.pressure_service.get_last_n_measurements(2)
        self.assertEqual(len(measurements_list), 2)
        measurements_list = self.pressure_service.get_last_n_measurements(10)
        self.assertEqual(len(measurements_list), measurements_num + 1)
        self.assertEqual(measurements_list[0].timestamp, self._old_time_stamp)

    def test_measurements_between(self):
        current_timestamp = get_current_timestamp()
        self.db_cursor.execute('INSERT INTO Pressure VALUES (?, ?);', (current_timestamp, 735,))
        measurements_list = self.pressure_service.get_measurements_between(get_current_timestamp() - 100,
                                                                           get_current_timestamp())
        self.assertEqual(len(measurements_list), 1)
        self.assertEqual(measurements_list[0].timestamp, current_timestamp)
        measurements_list = self.pressure_service.get_measurements_between(self._old_time_stamp - 100,
                                                                           self._old_time_stamp)
        self.assertEqual(len(measurements_list), 1)
        self.assertEqual(measurements_list[0].timestamp, self._old_time_stamp)
