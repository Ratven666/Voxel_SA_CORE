from abc import ABC, abstractmethod


class ScanSamplerABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def __str__(self):
        return f"Разрядитель точек типа: {self.__class__.__name__}"

    @abstractmethod
    def do_sampling(self, scan):
        pass
