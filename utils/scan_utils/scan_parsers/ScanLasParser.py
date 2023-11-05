import laspy


from CONFIG import POINTS_CHUNK_COUNT, FILE_NAME
from utils.scan_utils.scan_parsers.ScanParserABC import ScanParserABC


class ScanLasParser(ScanParserABC):

    __supported_file_extension__ = [".las"]

    def __init__(self, chunk_count=POINTS_CHUNK_COUNT):
        self.__chunk_count = chunk_count
        self.__last_point_id = None

    @staticmethod
    def __get_xyz(not_scaled_xyz, scales, offsets):
        xyz = []
        for idx, coord in enumerate(not_scaled_xyz):
            xyz.append(coord * scales[idx] + offsets[idx])
        return xyz

    @staticmethod
    def __get_rgb(not_scaled_rgb):
        COLOR_SCALE = 0.003906309605554284
        return [int(r_g_b * COLOR_SCALE) for r_g_b in not_scaled_rgb]

    def parse(self, file_name=FILE_NAME):
        """
        Запускает процедуру парсинга файла и возвращает списки словарей с данными для загрузки в БД
        размером не превышающим POINTS_CHUNK_COUNT
        При запуске выполняется процедурка проверки расширения файла
        :param file_name: путь до файла из которго будут загружаться данные
        :return: список точек готовый к загрузке в БД
        """
        self._check_file_extension(file_name, self.__supported_file_extension__)
        self.__last_point_id = self._get_last_point_id()

        with laspy.open(file_name) as input_las:
            for points in input_las.chunk_iterator(self.__chunk_count):
                offsets = points.offsets
                scales = points.scales
                points = points.array
                points_to_db = []
                for point in points:
                    xyz = self.__get_xyz((point[0], point[1], point[2]), offsets=offsets, scales=scales)
                    rgb = self.__get_rgb((point[-3], point[-2], point[-1]))
                    self.__last_point_id += 1
                    point = {"id": self.__last_point_id,
                             "X": xyz[0], "Y": xyz[1], "Z": xyz[2],
                             "R": rgb[0], "G": rgb[1], "B": rgb[2]
                             }
                    points_to_db.append(point)
                yield points_to_db
