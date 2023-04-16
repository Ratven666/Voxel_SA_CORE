import logging
from abc import ABC, abstractmethod

from sqlalchemy import delete

from CONFIG import LOGGER
from classes.ScanDB import ScanDB
from utils.scan_utils.Scan_metrics import update_scan_in_db_from_scan, update_scan_metrics
from utils.start_db import engine, Tables


class ScanFilterABC(ABC):
    logger = logging.getLogger(LOGGER)

    def __init__(self, scan):
        self.scan = scan

    def __scan_name_generator(self):
        return f"{self.scan.scan_name}_FB_{self.__class__.__name__}" \
               f"_FROM_{self.dem_model.model_name}"

    @abstractmethod
    def _filter_logic(self, point):
        pass

    def filter_scan(self):
        points = []
        for point in self.scan:
            if self._filter_logic(point) is True:
                points.append(({"point_id": point.id,
                                "scan_id": self.scan.id}))
        with engine.connect() as db_connection:
            stmt = delete(Tables.points_scans_db_table)\
                    .where(Tables.points_scans_db_table.c.scan_id == self.scan.id)
            db_connection.execute(stmt)
            db_connection.execute(Tables.points_scans_db_table.insert(), points)
            db_connection.commit()
        update_scan_metrics(self.scan)
        update_scan_in_db_from_scan(self.scan)
        return self.scan

    def create_new_filtered_scan(self, force_filter=False):
        new_scan = ScanDB(self.__scan_name_generator())
        points = []
        if len(new_scan) != 0:
            if force_filter:
                with engine.connect() as db_connection:
                    stmt = delete(Tables.points_scans_db_table) \
                        .where(Tables.points_scans_db_table.c.scan_id == new_scan.id)
                    db_connection.execute(stmt)
                    db_connection.commit()
            else:
                self.logger.warning(f"Скан {self.scan.scan_name} уже отфильтрован с такими параметрами")
                return new_scan
        for point in self.scan:
            if self._filter_logic(point) is True:
                points.append(({"point_id": point.id,
                                "scan_id": new_scan.id}))
        with engine.connect() as db_connection:
            db_connection.execute(Tables.points_scans_db_table.insert(), points)
            db_connection.commit()
        update_scan_metrics(new_scan)
        update_scan_in_db_from_scan(new_scan)
        return new_scan
