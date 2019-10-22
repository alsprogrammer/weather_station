from typing import Union
from unittest import TestCase

from measurement_updater.getters.measurement_getter_abc import MeasurementGetter
from measurement_updater.measurement_updater import MeasurementUpdater
from measurement_updater.senders.sender_abc import MeasurementSender
from utils.time_utils import get_current_timestamp

MEASUREMENT_VALUE = 735


class MockMeasurementGetter(MeasurementGetter):
    def __call__(self):
        return MEASUREMENT_VALUE


class MockMeasurementSender(MeasurementSender):
    def __call__(self, value: Union[int, float], timestamp: int):
        self.value = value
        self.timestamp = timestamp


class TestMeasurementUpdater(TestCase):
    def setUp(self) -> None:
        self.getter = MockMeasurementGetter()
        self.sender = MockMeasurementSender()

        self.updater = MeasurementUpdater(self.getter, self.sender)

    def test_get_and_send_measurement(self):
        timestamp_before = get_current_timestamp()
        self.updater.get_and_send_measurement()
        timestamp_after = get_current_timestamp()
        self.assertEqual(self.sender.value, MEASUREMENT_VALUE)
        self.assertGreaterEqual(self.sender.timestamp, timestamp_before)
        self.assertLessEqual(self.sender.timestamp, timestamp_after)
