from measurement_updater import MeasurementUpdater
from senders.rest_api_sender import RESTApiMeasurementSender

from config import *

if __name__ == "__main__":
    sender = RESTApiMeasurementSender(URL)
    service = MeasurementUpdater(sender=sender)
    service.get_and_send_measurement()
