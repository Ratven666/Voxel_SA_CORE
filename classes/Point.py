from classes.abc_classes.PointABC import PointABC


class Point(PointABC):
    """Класс точки"""

    __slots__ = []

    @classmethod
    def parse_point_from_db_row(cls, row: tuple):
        """
        Метод который создает и возвращает объект Point по данным читаемым из БД
        :param row: кортеж данных читаемых из БД
        :return: объект класса Point
        """
        return cls(id_=row[0], X=row[1], Y=row[2], Z=row[3], R=row[4], G=row[5], B=row[6])


if __name__ == "__main__":
    p1 = Point(1, 2, 3, 4, 5, 6, id_=12)
    p2 = Point(10, 20, 30, 40, 50, 60)
    print(p1)
    print(p2)
    point_list = [p1, p2]
    print(point_list)
