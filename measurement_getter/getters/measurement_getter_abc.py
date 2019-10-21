from abc import ABC, abstractmethod


class MeasurementGetter(ABC):
    @abstractmethod
    def __call__(self):
        raise NotImplementedError()
