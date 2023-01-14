from classes.abc_classes.PointABC import PointABC


class Point(PointABC):
    __slots__ = []

    @classmethod
    def parse_point_from_db_row(cls, row: tuple):
        return cls(id_=row[0], X=row[1], Y=row[2], Z=row[3], R=row[4], G=row[5], B=row[6])
