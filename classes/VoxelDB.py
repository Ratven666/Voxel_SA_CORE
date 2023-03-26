from sqlalchemy import select, insert, delete

from classes.ScanDB import ScanDB
from classes.abc_classes.VoxelABC import VoxelABC
from utils.start_db import Tables, engine


class VoxelDB(VoxelABC):
    """
    Воксель связанный с базой данных
    """

    __slots__ = ["id", "X", "Y", "Z", "step", "vxl_mdl_id", "vxl_name", "scan_id", "len", "R", "G", "B", "scan"]

    def __init__(self, X, Y, Z, step, vxl_mdl_id):
        super().__init__(X, Y, Z, step, vxl_mdl_id)
        self.scan = None
        self.__init_voxel()

    @staticmethod
    def delete_voxel(voxel_id):
        """
        Удаляет запись вокселя из БД
        :param voxel_id: id вокселя который требуется удалить из БД
        :return: None
        """
        with engine.connect() as db_connection:
            stmt = delete(Tables.voxels_db_table).where(Tables.voxels_db_table.c.id == voxel_id)
            db_connection.execute(stmt)
            db_connection.commit()

    def __init_voxel(self):
        """
        Инициализирует воксель при запуске
        Если воксель с таким именем уже есть в БД - запускает копирование данных из БД в атрибуты скана
        Если такого вокселя нет - создает новую запись в БД
        :return: None
        """
        select_ = select(Tables.voxels_db_table).where(Tables.voxels_db_table.c.vxl_name == self.vxl_name)

        with engine.connect() as db_connection:
            db_voxel_data = db_connection.execute(select_).mappings().first()
            if db_voxel_data is not None:
                self.__copy_voxel_data(db_voxel_data)
                self.scan = ScanDB(f"SC_{self.vxl_name}")
            else:
                scan = ScanDB(f"SC_{self.vxl_name}")
                stmt = insert(Tables.voxels_db_table).values(vxl_name=self.vxl_name,
                                                             X=self.X,
                                                             Y=self.Y,
                                                             Z=self.Z,
                                                             step=self.step,
                                                             scan_id=scan.id,
                                                             vxl_mdl_id=self.vxl_mdl_id,
                                                             )
                db_connection.execute(stmt)
                db_connection.commit()
                self.__init_voxel()

    def __copy_voxel_data(self, db_voxel_data: dict):
        """
        Копирует данные записи из БД в атрибуты вокселя
        :param db_voxel_data: Результат запроса к БД
        :return: None
        """
        self.id = db_voxel_data["id"]
        self.X = db_voxel_data["X"]
        self.Y = db_voxel_data["Y"]
        self.Z = db_voxel_data["Z"]
        self.step = db_voxel_data["step"]
        self.vxl_mdl_id = db_voxel_data["vxl_mdl_id"]
        self.vxl_name = db_voxel_data["vxl_name"]
        self.scan_id = db_voxel_data["scan_id"]
        self.len = db_voxel_data["len"]
        self.R = db_voxel_data["R"]
        self.G = db_voxel_data["G"]
        self.B = db_voxel_data["B"]
