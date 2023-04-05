from sqlalchemy import select, insert
import numpy as np

from classes.PlaneCellDB import PlaneCellDB
from classes.ScanDB import ScanDB
from classes.abc_classes.SegmentedModelABC import SegmentedModelABC
from utils.start_db import Tables, engine


class PlaneModelDB(SegmentedModelABC):
    """
    DEM модель связанная с базой данных
    """
    db_table = Tables.plane_models_db_table

    def __init__(self, voxel_model):
        super().__init__(voxel_model, PlaneCellDB)
        self.model_name = f"PLANE_from_{self.voxel_model.vm_name}"
        self.mse_data = None
        self.__init_plane_mdl()

    def __init_plane_mdl(self):
        select_ = select(self.db_table) \
            .where(self.db_table.c.base_voxel_model_id == self.voxel_model.id)

        with engine.connect() as db_connection:
            db_plane_model_data = db_connection.execute(select_).mappings().first()
            if db_plane_model_data is not None:
                self._copy_model_data(db_plane_model_data)
                self._load_cell_data_from_db(db_connection)
                self.logger.info(f"Загрузка PLANE модели завершена")
            else:
                stmt = insert(self.db_table).values(base_voxel_model_id=self.voxel_model.id,
                                                    plane_model_name=self.model_name,
                                                    MSE_data=self.mse_data
                                                    )
                db_connection.execute(stmt)
                db_connection.commit()
                self.id = self._get_last_model_id()
                self._calk_segment_model()
                self._calk_model_mse(db_connection)
                self._save_cell_data_in_db(db_connection)
                db_connection.commit()
                self.logger.info(f"Расчет PLANE модели завершен и загружен в БД")

    def _calk_segment_model(self):
        base_scan = ScanDB.get_scan_from_id(self.voxel_model.base_scan_id)
        self.__fit_planes(base_scan)
        self.__calk_mse(base_scan)

    def __fit_planes(self, base_scan):
        self.logger.info(f"Начат расчет элементов матрицы нормальных коэфициентов завершен")
        self.__calk_matrix_params(base_scan)
        self.logger.info(f"Рассчет элементов матрицы нормальных коэфициентов завершен")
        self.logger.info(f"Начат расчет параметров вписываемых плоскостей завершен")
        for cell in self:
            try:
                m_a = np.array([[cell.a1, cell.b1, cell.c1],
                                [cell.b1, cell.b2, cell.c2],
                                [cell.c1, cell.c2, cell.c3]])
                m_d = np.array([cell.d1, cell.d2, cell.d3])
            except AttributeError:
                continue
            try:
                abc = np.linalg.solve(m_a, m_d)
            except np.linalg.LinAlgError:
                cell.r = -1
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
            cell_z = cell.get_z_from_xy(point.X, point.Y)
            if cell_z is None:
                continue
            try:
                cell.vv += (point.Z - cell_z) ** 2
            except AttributeError:
                cell.vv = (point.Z - cell_z) ** 2
        for cell in self._model_structure.values():
            if cell.r > 0:
                cell.mse = (cell.vv / cell.r) ** 0.5
        self.logger.info(f"Расчет СКП высот завершен")

    def _copy_model_data(self, db_model_data: dict):
        self.id = db_model_data["id"]
        self.base_voxel_model_id = db_model_data["base_voxel_model_id"]
        self.plane_model_name = db_model_data["plane_model_name"]
        self.mse_data = db_model_data["MSE_data"]
