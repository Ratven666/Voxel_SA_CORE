from sqlalchemy import insert

from classes.abc_classes.CellABC import CellABC
from utils.start_db import Tables


class SubsidenceCellDB(CellABC):
    db_table = Tables.subsidence_cell_db_table

    def __init__(self, voxel, dem_model):
        self.voxel = voxel
        self.dem_model = dem_model
        self.voxel_id = None
        self.subsidence = None
        self.subsidence_mse = None

    def get_z_from_xy(self, x, y):
        """
        Рассчитывает отметку точки (x, y) в ячейке
        :param x: координата x
        :param y: координата y
        :return: координата z для точки (x, y)
        """
        return self.subsidence

    def get_mse_z_from_xy(self, x, y):
        return self.subsidence_mse

    def get_db_raw_data(self):
        return {"voxel_id": self.voxel.id,
                "base_model_id": self.dem_model.id,
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
                                            base_model_id=self.dem_model.id,
                                            subsidence=self.subsidence,
                                            subsidence_mse=self.subsidence_mse,
                                            )
        db_connection.execute(stmt)

    def _copy_cell_data(self, db_cell_data):
        """
        Копирует данные из записи БД в атрибуты ячейки
        :param db_cell_data: загруженные из БД данные
        :return: None
        """
        self.voxel_id = db_cell_data["voxel_id"]
        self.base_model_id = db_cell_data["base_model_id"]
        self.subsidence = db_cell_data["subsidence"]
        self.subsidence_mse = db_cell_data["subsidence_mse"]

    def __str__(self):
        return f"{self.__class__.__name__} [ID: {self.voxel.id},\tavr_z: {self.subsidence:.3f}\t" \
               f"MSE: {self.subsidence_mse:.3f}\tr: {self.r}]"

    def __repr__(self):
        return f"{self.__class__.__name__} [ID: {self.voxel.id}]"
