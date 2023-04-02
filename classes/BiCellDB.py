from sqlalchemy import select, insert, and_

from classes.abc_classes.CellABC import CellABC
from utils.start_db import Tables


class BiCellDB(CellABC):
    db_table = Tables.bi_cell_db_table

    def __init__(self, cell, bi_model):
        self.cell = cell
        self.voxel = cell.voxel
        self.bi_model = bi_model
        self.voxel_id = None
        self.base_bi_model_id = None
        self.left_down = {"X": self.voxel.X, "Y": self.voxel.Y, "Z": None, "MSE": None}
        self.left_up = {"X": self.voxel.X, "Y": self.voxel.Y + self.voxel.step, "Z": None, "MSE": None}
        self.right_down = {"X": self.voxel.X + self.voxel.step, "Y": self.voxel.Y, "Z": None, "MSE": None}
        self.right_up = {"X": self.voxel.X + self.voxel.step, "Y": self.voxel.Y + self.voxel.step, "Z": None,
                         "MSE": None}
        self.mse = None

    def get_z_from_xy(self, x, y):
        x1, x2 = self.left_down["X"], self.right_down["X"]
        y1, y2 = self.left_down["Y"], self.left_up["Y"]
        r1 = ((x2 - x)/(x2 - x1)) * self.left_down["Z"] + ((x - x1)/(x2 - x1)) * self.right_down["Z"]
        r2 = ((x2 - x)/(x2 - x1)) * self.left_up["Z"] + ((x - x1)/(x2 - x1)) * self.right_up["Z"]
        z = ((y2 - y)/(y2 - y1)) * r1 + ((y - y1)/(y2 - y1)) * r2
        return z

    def _load_cell_data_from_db(self, db_connection):
        select_ = select(self.db_table) \
            .where(and_(self.db_table.c.voxel_id == self.voxel.id,
                        self.db_table.c.base_bi_model_id == self.bi_model.id))
        db_cell_data = db_connection.execute(select_).mappings().first()
        if db_cell_data is not None:
            self._copy_cell_data(db_cell_data)

    def _save_cell_data_in_db(self, db_connection):
        stmt = insert(self.db_table).values(voxel_id=self.voxel.id,
                                            base_bi_model_id=self.bi_model.id,
                                            Z_ld=self.left_down["Z"],
                                            Z_lu=self.left_up["Z"],
                                            Z_rd=self.right_down["Z"],
                                            Z_ru=self.right_up["Z"],
                                            MSE_ld=self.left_down["MSE"],
                                            MSE_lu=self.left_up["MSE"],
                                            MSE_rd=self.right_down["MSE"],
                                            MSE_ru=self.right_up["MSE"],
                                            MSE=self.mse,
                                            )
        db_connection.execute(stmt)

    def _copy_cell_data(self, db_cell_data):
        self.voxel_id = db_cell_data["voxel_id"]
        self.base_bi_model_id = db_cell_data["base_bi_model_id"]
        self.base_bi_model_id = db_cell_data["base_bi_model_id"]
        self.left_down["Z"], self.left_down["MSE"] = db_cell_data["Z_ld"], db_cell_data["MSE_ld"]
        self.left_up["Z"], self.left_up["MSE"] = db_cell_data["Z_lu"], db_cell_data["MSE_lu"]
        self.right_down["Z"], self.right_down["MSE"] = db_cell_data["Z_rd"], db_cell_data["MSE_rd"]
        self.right_up["Z"], self.right_down["MSE"] = db_cell_data["Z_ru"], db_cell_data["MSE_ru"]
        self.mse = db_cell_data["MSE"]

    def __str__(self):
        return f"{self.__class__.__name__} [ID: {self.voxel.id},\tbi_model: {self.bi_model}\t" \
               f"MSE: {self.mse:.3f}\tlen: {self.voxel.len}]"

    def __repr__(self):
        return f"{self.__class__.__name__} [ID: {self.voxel.id}]"
