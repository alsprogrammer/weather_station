from typing import Union

import requests

from senders.sender_abc import MeasurementSender


class RESTApiMeasurementSender(MeasurementSender):
    def __init__(self, url: str):
        self._url = url

    def __call__(self, value: Union[int, float], timestamp: int):
        requests.post(self._url, data={'value': value, 'timestamp': timestamp})
