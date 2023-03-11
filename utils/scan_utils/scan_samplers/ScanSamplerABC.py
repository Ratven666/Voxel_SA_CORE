from abc import ABC, abstractmethod


class ScanSamplerABC(ABC):
    """
    Абстрактный разрядитель плотности точек в скане
    """
    @abstractmethod
    def __init__(self):
        pass

    def __str__(self):
        return f"Разрядитель точек типа: {self.__class__.__name__}"

    @abstractmethod
    def do_sampling(self, scan):
        """
        Запускает процедуру разряжения плотности точек в скане
        :param scan: скан который требуется разрядить
        :return: разряженный скан типа ScanLite (в оперативной памяти)
        """
        pass
