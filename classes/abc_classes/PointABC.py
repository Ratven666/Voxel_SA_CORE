from abc import ABC


class PointABC(ABC):
    """Абстрактный класс точки"""

    __slots__ = ["id", "X", "Y", "Z", "R", "G", "B"]

    def __init__(self, X, Y, Z, R, G, B, id_=None):
        self.id = id_
        self.X, self.Y, self.Z = X, Y, Z
        self.R, self.G, self.B = R, G, B

    def __str__(self):
        return f"{self.__class__.__name__} " \
               f"[id: {self.id},\tx: {self.X} y: {self.Y} z: {self.Z},\t" \
               f"RGB: ({self.R},{self.G},{self.B})]"

    def __repr__(self):
        return f"{self.__class__.__name__} [id: {self.id}]"
