from sqlalchemy import select, insert

from classes.abc_classes.CellABC import CellABC
from utils.start_db import Tables


class PlaneCellDB(CellABC):

    def __init__(self, voxel):
        self.voxel = voxel
        self.voxel_id = None
        self.a = None
        self.b = None
        self.d = None
        self.mse = None

    def get_z_from_xy(self, x, y):
        try:
            z = self.a * x + self.b * y + self.d
        except TypeError:
            z = None
        return z

    def _load_cell_data_from_db(self, db_connection):
        select_ = select(Tables.plane_cell_db_table) \
                 .where(Tables.plane_cell_db_table.c.voxel_id == self.voxel.id)
        db_plane_cell_data = db_connection.execute(select_).mappings().first()
        if db_plane_cell_data is not None:
            self._copy_cell_data(db_plane_cell_data)

    def _save_cell_data_in_db(self, db_connection):
        stmt = insert(Tables.plane_cell_db_table).values(voxel_id=self.voxel.id,
                                                         A=self.a,
                                                         B=self.b,
                                                         D=self.d,
                                                         MSE=self.mse
                                                         )
        db_connection.execute(stmt)

    def _copy_cell_data(self, db_plane_cell_data):
        self.voxel_id = db_plane_cell_data["voxel_id"]
        self.a = db_plane_cell_data["A"]
        self.b = db_plane_cell_data["B"]
        self.d = db_plane_cell_data["D"]
        self.mse = db_plane_cell_data["MSE"]

    def __str__(self):
        return f"{self.__class__.__name__} [ID: {self.voxel.id},\t" \
               f"Z = {self.a:.3f}*X + {self.b:.3f}*Y +{self.d:.3f}\t" \
               f"MSE: {self.mse:.3f},\tlen: {self.voxel.len}]"

    def __repr__(self):
        return f"{self.__class__.__name__} [ID: {self.voxel.id}]"
