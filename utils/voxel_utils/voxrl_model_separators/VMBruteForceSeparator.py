from os import remove

from CONFIG import POINTS_CHUNK_COUNT
from classes.ScanDB import ScanDB
from classes.VoxelDB import VoxelDB
from utils.scan_utils.Scan_metrics import update_scan_borders, update_scan_in_db_from_scan
from utils.start_db import engine, Tables
from utils.voxel_utils.Voxel_metrics import update_voxel_in_db_from_voxel
from utils.voxel_utils.Voxel_model_metrics import update_voxel_model_in_db_from_voxel_model
from utils.voxel_utils.voxel_model_iterators.VMFullBaseIterator import VMFullBaseIterator
from utils.voxel_utils.voxrl_model_separators.VMSeparatorABC import VMSeparatorABC


class VMBruteForceSeparator(VMSeparatorABC):

    def __init__(self):
        self.voxel_model = None
        self.voxel_structure = None

    def separate_voxel_model(self, voxel_model, scan):
        self.__create_full_vxl_struct(voxel_model)
        voxel_model.logger.info(f"Структура {voxel_model.vm_name} создана")
        self.__separate_scan_to_vxl(scan)
        voxel_model.logger.info(f"Разбиение скана {scan.scan_name} в {voxel_model.vm_name} законченно")
        self.__calk_scan_metrics_in_voxels()
        voxel_model.logger.info(f"Расчет метрик сканов завершен и загружен в БД")

    def __create_full_vxl_struct(self, voxel_model):
        self.voxel_model = voxel_model
        self.voxel_structure = [[[VoxelDB(voxel_model.min_X + x * voxel_model.step,
                                  voxel_model.min_Y + y * voxel_model.step,
                                  voxel_model.min_Z + z * voxel_model.step,
                                  voxel_model.step, voxel_model.id)
                                for x in range(voxel_model.X_count)]
                                for y in range(voxel_model.Y_count)]
                                for z in range(voxel_model.Z_count)]
        self.voxel_model.voxel_structure = self.voxel_structure

    def __separate_scan_to_vxl(self, scan):
        self.__write_temp_points_scans_file(scan)
        with engine.connect() as db_connection:
            for data in self.__parse_temp_points_scans_file():
                db_connection.execute(Tables.points_scans_db_table.insert(), data)
                self.voxel_model.logger.info(f"Пакет точек загружен в БД")
            db_connection.commit()

    def __write_temp_points_scans_file(self, scan):
        with open("temp_file.txt", "w", encoding="UTF-8") as file:
            for point in scan:
                vxl_md_X = int((point.X - self.voxel_model.min_X) // self.voxel_model.step)
                vxl_md_Y = int((point.Y - self.voxel_model.min_Y) // self.voxel_model.step)
                if self.voxel_model.is_2d_vxl_mdl:
                    vxl_md_Z = 0
                else:
                    vxl_md_Z = int((point.Z - self.voxel_model.min_Z) // self.voxel_model.step)
                scan_id = self.voxel_structure[vxl_md_Z][vxl_md_Y][vxl_md_X].scan_id
                file.write(f"{point.id}, {scan_id}\n")
                self.__update_scan_data(self.voxel_structure[vxl_md_Z][vxl_md_Y][vxl_md_X].scan,
                                        point)
                self.__update_voxel_data(self.voxel_structure[vxl_md_Z][vxl_md_Y][vxl_md_X], point)

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

    @staticmethod
    def __parse_temp_points_scans_file():
        points_scans = []
        try:
            with open("temp_file.txt", "r", encoding="UTF-8") as file:
                for line in file:
                    data = [int(p_ps) for p_ps in line.strip().split(",")]
                    points_scans.append({"point_id": data[0], "scan_id": data[1]})
                    if len(points_scans) == POINTS_CHUNK_COUNT:
                        yield points_scans
                        points_scans = []
            yield points_scans
        finally:
            try:
                remove("temp_file.txt")
            except FileNotFoundError:
                pass

    def __calk_scan_metrics_in_voxels(self):
        voxel_counter = 0
        for voxel in iter(VMFullBaseIterator(self.voxel_model)):
            if len(voxel) == 0:
                VoxelDB.delete_voxel(voxel.id)
                ScanDB.delete_scan(voxel.scan_id)
            else:
                update_scan_in_db_from_scan(voxel.scan)
                update_voxel_in_db_from_voxel(voxel)
                voxel_counter += 1
        self.voxel_model.len = voxel_counter
        update_voxel_model_in_db_from_voxel_model(self.voxel_model)
