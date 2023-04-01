from sqlalchemy import select, insert

from utils.start_db import Tables


class DemCellDB:

    def __init__(self, voxel):
        self.voxel = voxel
        self.voxel_id = None
        self.avr_z = 0
        self.mse = 0

    def _load_cell_data_from_db(self, db_connection):
        select_ = select(Tables.dem_cell_db_table) \
                 .where(Tables.dem_cell_db_table.c.voxel_id == self.voxel.id)
        db_dem_cell_data = db_connection.execute(select_).mappings().first()
        if db_dem_cell_data is not None:
            self.__copy_dem_cell_data(db_dem_cell_data)

    def _save_cell_data_in_db(self, db_connection):
        stmt = insert(Tables.dem_cell_db_table).values(voxel_id=self.voxel.id,
                                                       Avr_Z=self.avr_z,
                                                       MSE=self.mse,
                                                       )
        db_connection.execute(stmt)

    def __copy_dem_cell_data(self, db_dem_cell_data):
        self.voxel_id = db_dem_cell_data["voxel_id"]
        self.avr_z = db_dem_cell_data["Avr_Z"]
        self.mse = db_dem_cell_data["MSE"]

    def __str__(self):
        return f"{self.__class__.__name__} [ID: {self.voxel.id},\tavr_z: {self.avr_z:.3f}\t" \
               f"MSE: {self.mse:.3f}\tlen: {self.voxel.len}]"

    def __repr__(self):
        return f"{self.__class__.__name__} [ID: {self.voxel.id}]"
