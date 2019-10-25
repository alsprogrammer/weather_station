from measurement_updaters.getters.measurement_getter_abc import MeasurementGetter
from measurement_updaters.senders.sender_abc import MeasurementSender
from utils.time_utils import get_current_timestamp


class MeasurementUpdater:
    def __init__(self, getter: MeasurementGetter, sender: MeasurementSender):
        self._getter = getter
        self._sender = sender

    def get_and_send_measurement(self):
        measurement = self._getter()
        timestamp = get_current_timestamp()
        self._sender(measurement, timestamp)
