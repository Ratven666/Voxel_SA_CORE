from sqlalchemy import select, insert

from CONFIG import FILE_NAME, POINTS_CHUNK_COUNT
from classes.abc_classes.ScanABC import ScanABC
from utils.scan_utils.ScanLoader import ScanLoader
from utils.parsers.ScanTxtParser import ScanTxtParser
from utils.scan_utils.scan_iterators.BaseScanIterator import BaseScanIterator
from utils.scan_utils.scan_iterators.ScanIterator import ScanIterator
from utils.scan_utils.scan_iterators.SqlLiteScanIterator import SqlLiteScanIterator
from utils.start_db import engine, Tables


class ScanDB(ScanABC):

    def __init__(self, scan_name):
        super().__init__(scan_name)
        self.__init_scan()

    def __iter__(self):
        return iter(ScanIterator(self))
        # return iter(SqlLiteScanIterator(self))
        # return iter(BaseScanIterator(self))

    def load_scan_from_file(self, scan_loader=ScanLoader(scan_parser=ScanTxtParser(chunk_count=POINTS_CHUNK_COUNT)),
                            file_name=FILE_NAME):
        scan_loader.load_data(self, file_name)

    def __init_scan(self):
        select_ = select(Tables.scans_db_table).where(Tables.scans_db_table.c.scan_name == self.scan_name)

        with engine.connect() as db_connection:
            db_scan_data = db_connection.execute(select_).mappings().first()
            if db_scan_data is not None:
                self.__copy_scan_data(db_scan_data)
            else:
                stmt = insert(Tables.scans_db_table).values(scan_name=self.scan_name)
                db_connection.execute(stmt)
                db_connection.commit()
                self.__init_scan()

    def __copy_scan_data(self, db_scan_data: dict):
        self.id = db_scan_data["id"]
        self.scan_name = db_scan_data["scan_name"]
        self.len = db_scan_data["len"]
        self.min_X, self.max_X = db_scan_data["min_X"], db_scan_data["max_X"]
        self.min_Y, self.max_Y = db_scan_data["min_Y"], db_scan_data["max_Y"]
        self.min_Z, self.max_Z = db_scan_data["min_Z"], db_scan_data["max_Z"]
