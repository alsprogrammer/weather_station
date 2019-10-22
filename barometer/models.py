from abc import ABC
from typing import Union

import time


class Measurement(ABC):
    timestamp: int
    value: Union[int, float]

    def __init__(self, value: Union[int, float], timestamp: int = None):
        self.timestamp = int(time.time() * 1000)  # datetime.datetime.timestamp(datetime.datetime.now())
        self.value = value
        if timestamp:
            self.timestamp = timestamp

    def __repr__(self):
        return "Measurement({}, {})".format(self.timestamp, self.value)


class PressureMeasurement(Measurement):
    value: int

    def __init__(self, pressure: int, timestamp: int = None):
        super(PressureMeasurement, self).__init__(pressure, timestamp)


if __name__ == "__main__":
    from time import sleep

    cur_measure = PressureMeasurement(735)
    print(cur_measure)

    sleep(1)

    new_measure = PressureMeasurement(745, int(time.time() * 1000))
    print(new_measure)
