import time

from getters.measurement_getter_abc import MeasurementGetter
from senders.sender_abc import MeasurementSender


class MeasurementUpdater:
    def __init__(self, getter: MeasurementGetter, sender: MeasurementSender):
        self._getter = getter
        self._sender = sender

    def get_and_send_measurement(self):
        measurement = self._getter()
        timestamp = int(time.time() * 1000)
        self._sender(measurement, timestamp)
