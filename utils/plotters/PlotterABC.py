from abc import ABC, abstractmethod


class PlotterABC(ABC):
    """
    Абстрактный класс плоттера данных
    """
    @abstractmethod
    def __init__(self):
        pass

    def __str__(self):
        return f"Плоттер типа: {self.__class__.__name__}"

    @abstractmethod
    def plot(self, scan):
        pass
