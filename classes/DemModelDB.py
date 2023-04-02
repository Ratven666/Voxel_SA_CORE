from sqlalchemy import select, insert

from classes.DemCellDB import DemCellDB
from classes.ScanDB import ScanDB
from classes.abc_classes.SegmentedModelABC import SegmentedModelABC
from utils.start_db import Tables, engine


class DemModelDB(SegmentedModelABC):
    """
    DEM модель связанная с базой данных
    """
    db_table = Tables.dem_models_db_table

    def __init__(self, voxel_model, min_voxel_len=1):
        super().__init__(voxel_model, DemCellDB, min_voxel_len)
        self.model_name = f"DEM_from_{self.voxel_model.vm_name}"
        self.mse_data = None
        self.__init_dem_mdl()

    def __init_dem_mdl(self):
        select_ = select(self.db_table) \
            .where(self.db_table.c.base_voxel_model_id == self.voxel_model.id)

        with engine.connect() as db_connection:
            db_dem_model_data = db_connection.execute(select_).mappings().first()
            if db_dem_model_data is not None:
                self._copy_model_data(db_dem_model_data)
                self._load_cell_data_from_db(db_connection)
                self.logger.info(f"Загрузка DEM модели завершена")
            else:
                stmt = insert(self.db_table).values(base_voxel_model_id=self.voxel_model.id,
                                                    dem_model_name=self.model_name,
                                                    MSE_data=self.mse_data
                                                    )
                db_connection.execute(stmt)
                db_connection.commit()
                self._calk_segment_model()
                self._save_cell_data_in_db(db_connection)
                db_connection.commit()
                self.logger.info(f"Расчет DEM модели завершен и загружен в БД")
                self.id = self._get_last_model_id()

    def _calk_segment_model(self):
        base_scan = ScanDB.get_scan_from_id(self.voxel_model.base_scan_id)
        self.__calk_average_z(base_scan)
        self.__calk_mse(base_scan)

    def __calk_average_z(self, base_scan):
        for point in base_scan:
            dem_cell = self.get_model_element_for_point(point)
            if dem_cell is None:
                continue
            try:
                dem_cell.avr_z = (dem_cell.avr_z * dem_cell.len + point.Z) / (dem_cell.len + 1)
                dem_cell.len += 1
            except AttributeError:
                dem_cell.avr_z = point.Z
                dem_cell.len = 1
        self.logger.info(f"Расчет средних высот завершен")

    def __calk_mse(self, base_scan):
        for point in base_scan:
            dem_cell = self.get_model_element_for_point(point)
            try:
                dem_cell.vv += (point.Z - dem_cell.avr_z) ** 2
            except AttributeError:
                dem_cell.vv = (point.Z - dem_cell.avr_z) ** 2
        for dem_cell in self._model_structure.values():
            try:
                dem_cell.mse = (dem_cell.vv / (dem_cell.len - 1)) ** 0.5
            except ZeroDivisionError:
                dem_cell.mse = None
        self.logger.info(f"Расчет СКП высот завершен")

    def _copy_model_data(self, db_model_data: dict):
        self.id = db_model_data["id"]
        self.base_voxel_model_id = db_model_data["base_voxel_model_id"]
        self.model_name = db_model_data["dem_model_name"]
        self.mse_data = db_model_data["MSE_data"]
