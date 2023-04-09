from sqlalchemy import insert

from classes.abc_classes.CellABC import CellABC
from utils.start_db import Tables


class PlaneCellDB(CellABC):
    """
    Класс ячейки модели с апроксимацией точек полскостью
    """

    db_table = Tables.plane_cell_db_table

    def __init__(self, voxel, dem_model):
        self.voxel = voxel
        self.dem_model = dem_model
        self.voxel_id = None
        self.a = None
        self.b = None
        self.d = None
        self.r = len(self.voxel) - 3
        self.mse = None

    def get_z_from_xy(self, x, y):
        """
        Рассчитывает отметку точки (x, y) в ячейке
        :param x: координата x
        :param y: координата y
        :return: координата z для точки (x, y)
        """
        try:
            z = self.a * x + self.b * y + self.d
            return z
        except TypeError:
            pass
        return None

    def _save_cell_data_in_db(self, db_connection):
        """
        Сохраняет данные ячейки из модели в БД
        :param db_connection: открытое соединение с БД
        :return: None
        """
        stmt = insert(Tables.plane_cell_db_table).values(voxel_id=self.voxel.id,
                                                         base_model_id=self.dem_model.id,
                                                         A=self.a,
                                                         B=self.b,
                                                         D=self.d,
                                                         r=self.r,
                                                         MSE=self.mse
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
        self.a = db_cell_data["A"]
        self.b = db_cell_data["B"]
        self.d = db_cell_data["D"]
        self.r = db_cell_data["r"]
        self.mse = db_cell_data["MSE"]

    def __str__(self):
        return f"{self.__class__.__name__} [ID: {self.voxel.id},\t" \
               f"Z = {self.a:.3f}*X + {self.b:.3f}*Y +{self.d:.3f}\t" \
               f"MSE: {self.mse:.3f},\tr: {self.r}]"

    def __repr__(self):
        return f"{self.__class__.__name__} [ID: {self.voxel.id}]"
