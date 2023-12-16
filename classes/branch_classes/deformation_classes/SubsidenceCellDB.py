from sqlalchemy import insert, select, and_

from classes.abc_classes.VoxelABC import VoxelABC
from utils.start_db import Tables


class SubsidenceCellDB:
    db_table = Tables.subsidence_cell_db_table

    def __init__(self, voxel, subsidence_model):
        self.voxel: VoxelABC = voxel
        self.subsidence_model = subsidence_model
        self.voxel_id = None
        self.subsidence = None
        self.subsidence_mse = None

    def get_subsidence_from_xy(self, x, y):
        """
        Рассчитывает отметку точки (x, y) в ячейке
        :param x: координата x
        :param y: координата y
        :return: координата z для точки (x, y)
        """
        return self.subsidence + self.subsidence_model.subsidence_offset

    def get_mse_z_from_xy(self, x, y):
        return self.subsidence_mse

    def get_db_raw_data(self):
        return {"voxel_id": self.voxel.id,
                "subsidence_model_id": self.subsidence_model.id_,
                "subsidence": self.subsidence,
                "subsidence_mse": self.subsidence_mse,
                }

    def _save_cell_data_in_db(self, db_connection):
        """
        Сохраняет данные ячейки из модели в БД
        :param db_connection: открытое соединение с БД
        :return: None
        """
        stmt = insert(self.db_table).values(voxel_id=self.voxel.id,
                                            subsidence_model_id=self.subsidence_model.id_,
                                            subsidence=self.subsidence,
                                            subsidence_mse=self.subsidence_mse,
                                            )
        db_connection.execute(stmt)

    def _load_cell_data_from_db(self, db_connection):
        """
        Загружает данные ячейки из БД в модель
        :param db_connection: открытое соединение с БД
        :return: None
        """
        select_ = select(self.db_table) \
            .where(and_(self.db_table.c.voxel_id == self.voxel.id,
                        self.db_table.c.subsidence_model_id == self.subsidence_model.id_))
        db_cell_data = db_connection.execute(select_).mappings().first()
        if db_cell_data is not None:
            self._copy_cell_data(db_cell_data)

    def _copy_cell_data(self, db_cell_data):
        """
        Копирует данные из записи БД в атрибуты ячейки
        :param db_cell_data: загруженные из БД данные
        :return: None
        """
        self.voxel_id = db_cell_data["voxel_id"]
        self.subsidence_model_id = db_cell_data["subsidence_model_id"]
        self.subsidence = db_cell_data["subsidence"]
        self.subsidence_mse = db_cell_data["subsidence_mse"]

    def __str__(self):
        return (f"{self.__class__.__name__} [ID: {self.voxel.id},\tsubsidence: "
                f"{round(self.subsidence, 3) if self.subsidence is not None else None}]")

    def __repr__(self):
        return f"{self.__class__.__name__} [ID: {self.voxel.id}]"
