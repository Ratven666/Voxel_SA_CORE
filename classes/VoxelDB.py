from sqlalchemy import select, insert, delete

from classes.ScanDB import ScanDB
from utils.start_db import Tables, engine


class VoxelDB:
    __slots__ = ["id", "X", "Y", "Z", "step", "scan_id", "vxl_mdl_id", "vxl_name"]

    def __init__(self, X, Y, Z, step, vxl_mdl_id):
        self.id = None
        self.X = X
        self.Y = Y
        self.Z = Z
        self.step = step
        self.scan_id = None
        self.vxl_mdl_id = vxl_mdl_id
        self.vxl_name = self.__name_generator()
        self.__init_voxel()

    @staticmethod
    def delete_voxel(voxel_id):
        with engine.connect() as db_connection:
            stmt = delete(Tables.voxels_db_table).where(Tables.voxels_db_table.c.id == voxel_id)
            db_connection.execute(stmt)
            db_connection.commit()

    def __name_generator(self):
        return (f"VXL_VM:{self.vxl_mdl_id}_s{self.step}_"
                f"X:{round(self.X, 5)}_"
                f"Y:{round(self.Y, 5)}_"
                f"Z:{round(self.Z, 5)}"
                )

    def __init_voxel(self):
        select_ = select(Tables.voxels_db_table).where(Tables.voxels_db_table.c.vxl_name == self.vxl_name)

        with engine.connect() as db_connection:
            db_voxel_data = db_connection.execute(select_).mappings().first()
            if db_voxel_data is not None:
                self.__copy_voxel_data(db_voxel_data)
            else:
                scan = ScanDB(f"SC_{self.vxl_name}")
                stmt = insert(Tables.voxels_db_table).values(vxl_name=self.vxl_name,
                                                             x0=self.X,
                                                             y0=self.Y,
                                                             z0=self.Z,
                                                             step=self.step,
                                                             scan_id=scan.id,
                                                             vxl_mdl_id=self.vxl_mdl_id,
                                                             )
                db_connection.execute(stmt)
                db_connection.commit()
                self.__init_voxel()

    def __copy_voxel_data(self, db_voxel_data: dict):
        self.id = db_voxel_data["id"]
        self.scan_id = db_voxel_data["scan_id"]

    def __str__(self):
        return (f"{self.__class__.__name__} "
                f"[id: {self.id},\tName: {self.vxl_name}\t\t"
                f"X: {round(self.X, 5)}\tY: {round(self.Y, 5)}\tZ: {round(self.Z, 5)}]"
                )

    def __repr__(self):
        return f"{self.__class__.__name__} [ID: {self.id}]"
