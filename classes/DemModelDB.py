from sqlalchemy import select, insert

from classes.DemCellDB import DemCellDB
from classes.ScanDB import ScanDB
from classes.abc_classes.SegmentedModelABC import SegmentedModelABC
from utils.segmented_mdl_utils.segmented_models_plotters.DemModelPlotterMPL import DemModelPlotterMPL
from utils.start_db import Tables, engine


class DemModelDB(SegmentedModelABC):
    """
    DEM модель связанная с базой данных
    """

    def __init__(self, voxel_model):
        super().__init__(voxel_model, DemCellDB)
        self.base_voxel_model_id = voxel_model.id
        self.dem_model_name = f"DEM_from_{self.voxel_model.vm_name}"
        self.mse_data = None
        self.__init_dem_mdl()

    def __iter__(self):
        return iter(self._model_structure.values())

    def plot(self, plotter=DemModelPlotterMPL()):
        plotter.plot(self)

    def __init_dem_mdl(self):
        select_ = select(Tables.dem_models_db_table) \
            .where(Tables.dem_models_db_table.c.base_voxel_model_id == self.voxel_model.id)

        with engine.connect() as db_connection:
            db_dem_model_data = db_connection.execute(select_).mappings().first()
            if db_dem_model_data is not None:
                self.__copy_dem_model_data(db_dem_model_data)
                self.__load_dem_cell_data_from_db(db_connection)
                self.logger.info(f"Загрузка DEM модели завершена")
            else:
                stmt = insert(Tables.dem_models_db_table).values(base_voxel_model_id=self.voxel_model.id,
                                                                 dem_model_name=self.dem_model_name
                                                                 )
                db_connection.execute(stmt)
                db_connection.commit()
                self._calk_segment_model()
                self.__save_dem_call_data_in_db(db_connection)
                db_connection.commit()
                self.logger.info(f"Рассчет DEM модели завершен и загружен в БД")

    def _calk_segment_model(self):
        base_scan = ScanDB.get_scan_from_id(self.voxel_model.base_scan_id)
        self.__calk_average_z(base_scan)
        self.__calk_mse(base_scan)

    def __load_dem_cell_data_from_db(self, db_connection):
        for dem_cell in self:
            dem_cell._load_dem_cell_data_from_db(db_connection)

    def __save_dem_call_data_in_db(self, db_connection):
        for dem_cell in self:
            dem_cell._save_dem_cell_data_in_db(db_connection)

    def __calk_average_z(self, base_scan):
        for point in base_scan:
            dem_cell = self.get_model_element_for_point(point)
            dem_cell.avr_z = (dem_cell.avr_z * dem_cell.len + point.Z) / (dem_cell.len + 1)
            dem_cell.len += 1
        self.logger.info(f"Рассчет средних высот завершен")

    def __calk_mse(self, base_scan):
        for point in base_scan:
            dem_cell = self.get_model_element_for_point(point)
            try:
                dem_cell.vv += (point.Z - dem_cell.avr_z) ** 2
            except AttributeError:
                dem_cell.vv = 0
        for dem_cell in self:
            try:
                dem_cell.mse = (dem_cell.vv / (dem_cell.len - 1)) ** 0.5
            except ZeroDivisionError:
                dem_cell.mse = float("inf")
        self.logger.info(f"Рассчет СКП высот завершен")

    def __copy_dem_model_data(self, db_dem_model_data: dict):
        self.base_voxel_model_id = db_dem_model_data["base_voxel_model_id"]
        self.dem_model_name = db_dem_model_data["dem_model_name"]
        self.mse_data = db_dem_model_data["MSE_data"]