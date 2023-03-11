from classes.abc_classes.PointABC import PointABC
from classes.abc_classes.ScanABC import ScanABC


class ScanLite(ScanABC):
    """
    Скан не связанный с базой данных
    Все данные, включая точки при переборе берутся из оперативной памяти
    """

    def __init__(self, scan_name):
        super().__init__(scan_name)
        self.__points = []

    def __iter__(self):
        return iter(self.__points)

    def add_point(self, point):
        if isinstance(point, PointABC):
            self.__points.append(point)
            self.len += 1
        else:
            raise TypeError(f"Можно добавить только объект точки. "
                             f"Переданно - {type(point)}, {point}")

    @classmethod
    def create_from_another_scan(cls, scan, copy_with_points=True):
        """
        Создает скан типа ScanLite и копирует в него данные из другого скана
        :param scan: копируемый скан
        :param copy_with_points: определяет нужно ли копировать скан вместе с точками
       :type copy_with_points: bool
        :return:
        """
        scan_lite = cls(scan.scan_name)
        scan_lite.id = scan.id
        scan_lite.len = 0
        scan_lite.min_X, scan_lite.min_Y, scan_lite.min_Z = scan.min_X, scan.min_Y, scan.min_Z
        scan_lite.max_X, scan_lite.max_Y, scan_lite.max_Z = scan.max_X, scan.max_Y, scan.max_Z
        if copy_with_points:
            scan_lite.__points = [point for point in scan]
            scan_lite.len = len(scan_lite.__points)
        return scan_lite
