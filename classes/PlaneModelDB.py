from sqlalchemy import select, insert
import numpy as np

from classes.PlaneCellDB import PlaneCellDB
from classes.ScanDB import ScanDB
from classes.abc_classes.SegmentedModelABC import SegmentedModelABC
from utils.segmented_mdl_utils.segmented_models_plotters.PlaneModelPlotterMPL import PlaneModelPlotterMPL
from utils.start_db import Tables, engine


class PlaneModelDB(SegmentedModelABC):
    """
    DEM модель связанная с базой данных
    """

    def __init__(self, voxel_model, min_voxel_len=3):
        super().__init__(voxel_model, PlaneCellDB, min_voxel_len=min_voxel_len)
        self.base_voxel_model_id = voxel_model.id
        self.model_name = f"PLANE_from_{self.voxel_model.vm_name}"
        self.mse_data = None
        self.__init_plane_mdl()

    def plot(self, plotter=PlaneModelPlotterMPL()):
        plotter.plot(self)

    def __init_plane_mdl(self):
        select_ = select(Tables.plane_models_db_table) \
            .where(Tables.plane_models_db_table.c.base_voxel_model_id == self.voxel_model.id)

        with engine.connect() as db_connection:
            db_plane_model_data = db_connection.execute(select_).mappings().first()
            if db_plane_model_data is not None:
                self._copy_model_data(db_plane_model_data)
                self._load_cell_data_from_db(db_connection)
                self.logger.info(f"Загрузка PLANE модели завершена")
            else:
                stmt = insert(Tables.plane_models_db_table).values(base_voxel_model_id=self.voxel_model.id,
                                                                   plane_model_name=self.model_name,
                                                                   MSE_data=self.mse_data
                                                                   )
                db_connection.execute(stmt)
                db_connection.commit()
                self._calk_segment_model()
                self._save_cell_data_in_db(db_connection)
                db_connection.commit()
                self.logger.info(f"Расчет DEM модели завершен и загружен в БД")

    def _calk_segment_model(self):
        base_scan = ScanDB.get_scan_from_id(self.voxel_model.base_scan_id)
        self.__fit_planes(base_scan)
        self.__calk_mse(base_scan)

    def __fit_planes(self, base_scan):
        self.logger.info(f"Начат расчет элементов материцы нормальных коэфициентов завершен")
        self.__calk_matrix_params(base_scan)
        self.logger.info(f"Рассчет элементов материцы нормальных коэфициентов завершен")
        self.logger.info(f"Начат расчет параметров вписываемых плоскостей завершен")
        for cell in self._model_structure.values():
            m_a = np.array([[cell.a1, cell.b1, cell.c1],
                            [cell.b1, cell.b2, cell.c2],
                            [cell.c1, cell.c2, cell.c3]])
            m_d = np.array([cell.d1, cell.d2, cell.d3])
            try:
                abc = np.linalg.solve(m_a, m_d)
            except np.linalg.LinAlgError:
                continue
            cell.a = float(abc[0])
            cell.b = float(abc[1])
            cell.d = float(abc[2])
        self.logger.info(f"Расчет параметров вписываемых плоскостей завершен")

    def __calk_matrix_params(self, base_scan):
        for point in base_scan:
            cell = self.get_model_element_for_point(point)
            try:
                cell.a1 += point.X ** 2
                cell.b1 += point.X * point.Y
                cell.c1 += point.X
                cell.b2 += point.Y ** 2
                cell.c2 += point.Y
                cell.c3 += 1
                cell.d1 += point.X * point.Z
                cell.d2 += point.Y * point.Z
                cell.d3 += point.Z
            except AttributeError:
                cell.a1 = point.X ** 2
                cell.b1 = point.X * point.Y
                cell.c1 = point.X
                cell.b2 = point.Y ** 2
                cell.c2 = point.Y
                cell.c3 = 1
                cell.d1 = point.X * point.Z
                cell.d2 = point.Y * point.Z
                cell.d3 = point.Z

    def __calk_mse(self, base_scan):
        for point in base_scan:
            cell = self.get_model_element_for_point(point)
            try:
                cell_z = cell.a * point.X + cell.b * point.Y + cell.d
            except TypeError:
                continue
            try:
                cell.vv += (point.Z - cell_z) ** 2
            except AttributeError:
                cell.vv = (point.Z - cell_z) ** 2
        for cell in self._model_structure.values():
            if len(cell.voxel) <= 3:
                cell.mse = None
            else:
                cell.mse = (cell.vv / (len(cell.voxel) - 3)) ** 0.5
        self.logger.info(f"Расчет СКП высот завершен")

    def _copy_model_data(self, db_model_data: dict):
        self.base_voxel_model_id = db_model_data["base_voxel_model_id"]
        self.plane_model_name = db_model_data["plane_model_name"]
        self.mse_data = db_model_data["MSE_data"]
