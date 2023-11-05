from CONFIG import POINTS_CHUNK_COUNT, FILE_NAME
from utils.scan_utils.scan_parsers.ScanParserABC import ScanParserABC


class ScanPtsParser(ScanParserABC):
    __supported_file_extension__ = [".pts"]

    def __init__(self, rgb_color=True, chunk_count=POINTS_CHUNK_COUNT):
        self.__chunk_count = chunk_count
        self.__last_point_id = None
        self.rgb_color = rgb_color

    def get_point_dict(self, line):
        line = line.strip().split()
        xyz = [float(x_y_z) for x_y_z in line[0:3]]
        if len(line) == 4:
            rgb = [int(line[3])] * 3
        elif len(line) == 6 or len(line) == 7:
            rgb = [int(r_g_b) for r_g_b in line[-3:]]
        else:
            rgb = [0, 0, 0]
        self.__last_point_id += 1
        point = {"id": self.__last_point_id,
                 "X": xyz[0], "Y": xyz[1], "Z": xyz[2],
                 "R": rgb[0], "G": rgb[1], "B": rgb[2]
                 }
        return point

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

        with open(file_name) as file:
            points_count = int(file.readline())
            points = []
            for line in file:
                point = self.get_point_dict(line)
                if point is not None:
                    points.append(point)
                if len(points) == self.__chunk_count:
                    yield points
                    points = []
            yield points
