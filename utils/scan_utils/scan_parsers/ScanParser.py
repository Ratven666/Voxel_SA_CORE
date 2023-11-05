from CONFIG import FILE_NAME
from utils.scan_utils.scan_parsers.ScanLasParser import ScanLasParser
from utils.scan_utils.scan_parsers.ScanParserABC import ScanParserABC
from utils.scan_utils.scan_parsers.ScanTxtParser import ScanTxtParser


class ScanParser(ScanParserABC):

    def __init__(self):
        self.__scan_parser = None

    def __chose_scan_parser(self, file_name):
        """
        Выбирает парсер скана на основании расширения переданного файла
        :return: None
        """
        parsers = {"txt": ScanTxtParser,
                   "las": ScanLasParser,
                   }
        file_extension = file_name.split('.')[-1]
        self.__scan_parser = parsers[file_extension]

    def parse(self, file_name=FILE_NAME):
        self.__chose_scan_parser(file_name)
        for points in self.__scan_parser().parse(file_name=file_name):
            yield points
