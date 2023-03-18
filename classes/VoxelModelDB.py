from os import remove

from sqlalchemy import select, insert, desc

from CONFIG import POINTS_CHUNK_COUNT
from classes.ScanDB import ScanDB
from classes.VoxelDB import VoxelDB
from classes.abc_classes.ScanABC import ScanABC
from classes.abc_classes.VoxelModelABC import VoxelModelABC
from utils.scan_utils.Scan_metrics import update_scan_borders, \
    update_scan_in_db_from_scan
from utils.start_db import Tables, engine
from utils.voxel_utils.Voxel_metrics import update_voxel_in_db_from_voxel
from utils.voxel_utils.Voxel_model_metrics import update_voxel_model_in_db_from_voxel_model
from utils.voxel_utils.voxel_model_iterators.VMFullBaseIterator import VMFullBaseIterator
from utils.voxel_utils.voxel_model_iterators.VMRawIterator import VMRawIterator


class VoxelModelDB(VoxelModelABC):

    def __init__(self, scan: ScanABC, step, is_2d_vxl_mdl=True):
        super().__init__(scan, step, is_2d_vxl_mdl)
        self.__init_vxl_mdl(scan)
        self.vxl_model = None

    def __iter__(self):
        return iter(VMRawIterator(self))

    def __init_vxl_mdl(self, scan):
        select_ = select(Tables.voxel_models_db_table).where(Tables.voxel_models_db_table.c.vm_name == self.vm_name)

        with engine.connect() as db_connection:
            db_vm_data = db_connection.execute(select_).mappings().first()
            if db_vm_data is not None:
                self.__copy_vm_data(db_vm_data)
            else:
                self.__calc_vxl_md_metric(scan)
                self.base_scan_id = scan.id
                stmt = insert(Tables.voxel_models_db_table).values(vm_name=self.vm_name,
                                                                   step=self.step,
                                                                   len=self.len,
                                                                   X_count=self.X_count,
                                                                   Y_count=self.Y_count,
                                                                   Z_count=self.Z_count,
                                                                   min_X=self.min_X,
                                                                   max_X=self.max_X,
                                                                   min_Y=self.min_Y,
                                                                   max_Y=self.max_Y,
                                                                   min_Z=self.min_Z,
                                                                   max_Z=self.max_Z,
                                                                   base_scan_id=self.base_scan_id
                                                                   )
                db_connection.execute(stmt)
                db_connection.commit()
                stmt = (select(Tables.voxel_models_db_table.c.id).order_by(desc("id")))
                self.id = db_connection.execute(stmt).first()[0]
                self.__create_full_vxl_struct()
                self.logger.info(f"Структура {self.vm_name} создана")
                self.__separate_scan_to_vxl(scan)
                self.logger.info(f"Разбиение скана {scan.scan_name} в {self.vm_name} законченно")
                self.__calk_scan_metrics_in_voxels()

    def __calc_vxl_md_metric(self, scan):
        if len(scan) == 0:
            return None
        self.min_X = scan.min_X // self.step * self.step
        self.min_Y = scan.min_Y // self.step * self.step
        self.min_Z = scan.min_Z // self.step * self.step

        self.max_X = (scan.max_X // self.step + 1) * self.step
        self.max_Y = (scan.max_Y // self.step + 1) * self.step
        self.max_Z = (scan.max_Z // self.step + 1) * self.step

        self.X_count = round((self.max_X - self.min_X) / self.step)
        self.Y_count = round((self.max_Y - self.min_Y) / self.step)
        if self.is_2d_vxl_mdl:
            self.Z_count = 1
        else:
            self.Z_count = round((self.max_Z - self.min_Z) / self.step)
        self.len = self.X_count * self.Y_count * self.Z_count

    def __copy_vm_data(self, db_vm_data: dict):
        self.id = db_vm_data["id"]
        self.vm_name = db_vm_data["vm_name"]
        self.step = db_vm_data["step"]
        self.len = db_vm_data["len"]
        self.X_count, self.Y_count, self.Z_count = db_vm_data["X_count"], db_vm_data["Y_count"], db_vm_data["Z_count"]
        self.min_X, self.max_X = db_vm_data["min_X"], db_vm_data["max_X"]
        self.min_Y, self.max_Y = db_vm_data["min_Y"], db_vm_data["max_Y"]
        self.min_Z, self.max_Z = db_vm_data["min_Z"], db_vm_data["max_Z"]
        self.base_scan_id = db_vm_data["base_scan_id"]
        if self.Z_count == 1:
            self.is_2d_vxl_mdl = True
        else:
            self.is_2d_vxl_mdl = False

    def __create_full_vxl_struct(self):
        self.vxl_model = [[[VoxelDB(self.min_X + x * self.step,
                                    self.min_Y + y * self.step,
                                    self.min_Z + z * self.step,
                                    self.step, self.id)
                            for x in range(self.X_count)]
                           for y in range(self.Y_count)]
                          for z in range(self.Z_count)]

    def __write_temp_points_scans_file(self, scan):
        with open("temp_file.txt", "w", encoding="UTF-8") as file:
            for point in scan:
                vxl_md_X = int((point.X - self.min_X) // self.step)
                vxl_md_Y = int((point.Y - self.min_Y) // self.step)
                if self.is_2d_vxl_mdl:
                    vxl_md_Z = 0
                else:
                    vxl_md_Z = int((point.Z - self.min_Z) // self.step)
                scan_id = self.vxl_model[vxl_md_Z][vxl_md_Y][vxl_md_X].scan_id
                file.write(f"{point.id}, {scan_id}\n")
                self.__update_scan_data(self.vxl_model[vxl_md_Z][vxl_md_Y][vxl_md_X].scan,
                                        point)
                self.__update_voxel_data(self.vxl_model[vxl_md_Z][vxl_md_Y][vxl_md_X], point)

    @staticmethod
    def __parse_temp_points_scans_file():
        points_scans = []
        with open("temp_file.txt", "r", encoding="UTF-8") as file:
            for line in file:
                data = [int(p_ps) for p_ps in line.strip().split(",")]
                points_scans.append({"point_id": data[0], "scan_id": data[1]})
                if len(points_scans) == POINTS_CHUNK_COUNT:
                    yield points_scans
                    points_scans = []
        remove("temp_file.txt")
        yield points_scans

    def __separate_scan_to_vxl(self, scan):
        self.__write_temp_points_scans_file(scan)
        with engine.connect() as db_connection:
            for data in self.__parse_temp_points_scans_file():
                db_connection.execute(Tables.points_scans_db_table.insert(), data)
                self.logger.info(f"Пакет точек загружен в БД")
            db_connection.commit()

    @staticmethod
    def __update_scan_data(scan, point):
        scan.len += 1
        update_scan_borders(scan, point)

    @staticmethod
    def __update_voxel_data(voxel: VoxelDB, point):
        voxel.R = (voxel.R * voxel.len + point.R) / (voxel.len + 1)
        voxel.G = (voxel.G * voxel.len + point.G) / (voxel.len + 1)
        voxel.B = (voxel.B * voxel.len + point.B) / (voxel.len + 1)
        voxel.len += 1

    def __calk_scan_metrics_in_voxels(self):
        voxel_counter = 0
        for voxel in iter(VMFullBaseIterator(self)):
            if len(voxel) == 0:
                VoxelDB.delete_voxel(voxel.id)
                ScanDB.delete_scan(voxel.scan_id)
            else:
                update_scan_in_db_from_scan(voxel.scan)
                update_voxel_in_db_from_voxel(voxel)
                voxel_counter += 1
        self.len = voxel_counter
        update_voxel_model_in_db_from_voxel_model(self)
        self.logger.info(f"Расчет метрик сканов завершен и загружен в БД")
