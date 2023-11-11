from sqlalchemy import insert

from classes.abc_classes.CellABC import CellABC
from utils.start_db import Tables


class Polynomial2CellDB(CellABC):
    """
    Класс ячейки модели с апроксимацией точек полскостью
    """

    db_table = Tables.polynomial_2_cell_db_table

    def __init__(self, voxel, dem_model):
        self.voxel = voxel
        self.dem_model = dem_model
        self.voxel_id = None
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None
        self.m_a, self.m_b, self.m_c = None, None, None
        self.m_d, self.m_e, self.m_f = None, None, None
        self.r = len(self.voxel) - 6
        self.mse = None

    def get_z_from_xy(self, x, y):
        """
        Рассчитывает отметку точки (x, y) в ячейке
        :param x: координата x
        :param y: координата y
        :return: координата z для точки (x, y)
        """
        x = x - (self.voxel.X + self.voxel.step / 2)
        y = y - (self.voxel.Y + self.voxel.step / 2)
        try:
            z = (self.a * x ** 2 +
                 self.b * y ** 2 +
                 self.c * x * y +
                 self.d * x +
                 self.e * y +
                 self.f)
            return z
        except TypeError:
            pass
        return None

    def get_mse_z_from_xy(self, x, y):
        x = x - (self.voxel.X + self.voxel.step / 2)
        y = y - (self.voxel.Y + self.voxel.step / 2)
        try:
            mse_z = (((2 * x) ** 2) * (self.m_a ** 2) +
                     ((2 * y) ** 2) * (self.m_b ** 2) +
                     ((x * y) ** 2) * (self.m_c ** 2) +
                     (x ** 2) * (self.m_d ** 2) +
                     (y ** 2) * (self.m_e ** 2) +
                     self.m_f ** 2) ** 0.5
            return mse_z
        except TypeError:
            return None

    def get_db_raw_data(self):
        return {"voxel_id": self.voxel.id,
                "base_model_id": self.dem_model.id,
                "A": self.a,
                "B": self.b,
                "C": self.b,
                "D": self.d,
                "E": self.d,
                "F": self.d,
                "mA": self.m_a,
                "mB": self.m_b,
                "mC": self.m_c,
                "mD": self.m_d,
                "mE": self.m_e,
                "mF": self.m_f,
                "r": self.r,
                "MSE": self.mse}

    def _save_cell_data_in_db(self, db_connection):
        """
        Сохраняет данные ячейки из модели в БД
        :param db_connection: открытое соединение с БД
        :return: None
        """
        stmt = insert(self.db_table).values(voxel_id=self.voxel.id,
                                            base_model_id=self.dem_model.id,
                                            A=self.a,
                                            B=self.b,
                                            C=self.c,
                                            D=self.d,
                                            E=self.e,
                                            F=self.f,
                                            mA=self.m_a,
                                            mB=self.m_b,
                                            mC=self.m_c,
                                            mD=self.m_d,
                                            mE=self.m_e,
                                            mF=self.m_f,
                                            r=self.r,
                                            MSE=self.mse,
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
        self.c = db_cell_data["C"]
        self.d = db_cell_data["D"]
        self.e = db_cell_data["E"]
        self.f = db_cell_data["F"]
        self.m_a = db_cell_data["mA"]
        self.m_b = db_cell_data["mB"]
        self.m_b = db_cell_data["mC"]
        self.m_d = db_cell_data["mD"]
        self.m_d = db_cell_data["mE"]
        self.m_d = db_cell_data["mF"]
        self.r = db_cell_data["r"]
        self.mse = db_cell_data["MSE"]

    def __str__(self):
        return f"{self.__class__.__name__} [ID: {self.voxel.id},\t" \
               f"Z = {self.a:.3f}*X^2 + {self.b:.3f}*Y^2 + {self.c:.3f}*XY + " \
               f"{self.d:.3f}*X + {self.e:.3f}*Y + {self.f:.3f}\t" \
               f"MSE: {self.mse:.3f},\tr: {self.r}]"

    def __repr__(self):
        return f"{self.__class__.__name__} [ID: {self.voxel.id}]"
