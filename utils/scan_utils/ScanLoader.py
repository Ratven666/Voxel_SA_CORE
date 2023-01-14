import logging

from classes.ImportedFileDB import ImportedFileDB
from utils.parsers.ScanParserABC import ScanParserABC
from utils.parsers.ScanTxtParser import ScanTxtParser
from utils.scan_utils.Scan_metrics import calc_scan_metrics, update_scan_in_db
from utils.start_db import Tables, engine


class ScanLoader:
    __logger = logging.getLogger("console")

    def __init__(self, scan_parser=ScanTxtParser()):
        self.__scan_parser = scan_parser

    def load_data(self, scan, file_name: str):
        imp_file = ImportedFileDB(file_name)

        if imp_file.is_file_already_imported_into_scan(scan):
            self.__logger.warning(f"Файл \"{file_name}\" уже загружен в скан \"{scan.scan_name}\"")
            return

        with engine.connect() as db_connection:
            for points in self.__scan_parser.parse(file_name):
                points_scans = self.__get_points_scans_list(scan, points)
                self.__insert_to_db(points, points_scans, db_connection)
            db_connection.commit()
        scan = calc_scan_metrics(scan)
        update_scan_in_db(scan)
        imp_file._insert_in_db(scan)


    @staticmethod
    def __get_points_scans_list(scan, points):
        points_scans = []
        for point in points:
            points_scans.append({"point_id": point["id"], "scan_id": scan.id})
        return points_scans

    @staticmethod
    def __insert_to_db(points, points_scans, db_engine_connection):
        db_engine_connection.execute(Tables.points_db_table.insert(), points)
        db_engine_connection.execute(Tables.points_scans_db_table.insert(), points_scans)

    @property
    def scan_parser(self):
        return self.__scan_parser

    @scan_parser.setter
    def scan_parser(self, parser: ScanParserABC):
        if isinstance(parser, ScanParserABC):
            self.__scan_parser = parser
        else:
            raise TypeError(f"Нужно передать объект парсера! "
                            f"Переданно - {type(parser)}, {parser}")
