from abc import ABC, abstractmethod
from typing import Union


class MeasurementSender(ABC):
    @abstractmethod
    def __call__(self, value: Union[int, float], timestamp: int):
        raise NotImplementedError()
