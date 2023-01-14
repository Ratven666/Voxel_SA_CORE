import logging

from CONFIG import FILE_NAME, POINTS_CHUNK_COUNT
from utils.parsers.ScanParserABC import ScanParserABC


class ScanTxtParser(ScanParserABC):
    __supported_file_extension__ = [".txt"]
    __logger = logging.getLogger("console")


    def __init__(self, chunk_count=POINTS_CHUNK_COUNT):
        self.__chunk_count = chunk_count
        self.__last_point_id = None

    def parse(self, file_name=FILE_NAME):
        self._check_file_extension(file_name, self.__supported_file_extension__)
        self.__last_point_id = self._get_last_point_id()

        with open(file_name, "rt", encoding="utf-8") as file:
            points = []
            for line in file:
                line = line.strip().split()
                self.__last_point_id += 1
                try:
                    point = {"id": self.__last_point_id,
                             "X": line[0], "Y": line[1], "Z": line[2],
                             "R": line[3], "G": line[4], "B": line[5]
                             }
                except IndexError:
                    self.__logger.critical(f"Структура \"{file_name}\" некорректна - \"{line}\"")
                    return
                points.append(point)
                if len(points) == self.__chunk_count:
                    yield points
                    points = []
            yield points
