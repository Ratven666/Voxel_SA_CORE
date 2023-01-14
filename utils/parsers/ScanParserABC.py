from abc import ABC, abstractmethod

from sqlalchemy import select, desc

from utils.start_db import engine, Tables


class ScanParserABC(ABC):

    def __str__(self):
        return f"Парсер типа: {self.__class__.__name__}"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def _check_file_extension(file_name, __supported_file_extensions__):
        file_extension = f".{file_name.split('.')[-1]}"
        if file_extension not in __supported_file_extensions__:
            raise TypeError(f"Неправильный для парсера тип файла. "
                            f"Ожидаются файлы типа: {__supported_file_extensions__}")

    @staticmethod
    def _get_last_point_id():
        with engine.connect() as db_connection:
            stmt = (select(Tables.points_db_table.c.id).order_by(desc("id")))
            last_point_id = db_connection.execute(stmt).first()
            if last_point_id:
                return last_point_id[0]
            else:
                return 0

    @abstractmethod
    def parse(self, file_name: str):
        pass
