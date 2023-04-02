from sqlalchemy import select, insert

from classes.BiCellDB import BiCellDB
from classes.Point import Point
from classes.ScanDB import ScanDB
from classes.abc_classes.SegmentedModelABC import SegmentedModelABC
from utils.start_db import Tables, engine


class BiModelDB(SegmentedModelABC):
    """
    DEM модель связанная с базой данных
    """
    db_table = Tables.bi_models_db_table

    def __init__(self, segment_model, min_voxel_len=1):
        self.segment_model = segment_model
        super().__init__(segment_model.voxel_model, BiCellDB, min_voxel_len)
        self.model_name = f"BI_from_{self.segment_model.model_name}"
        self.mse_data = None
        self.__init_bi_mdl()

    def __init_bi_mdl(self):
        select_ = select(self.db_table) \
            .where(self.db_table.c.base_segment_model_name == self.segment_model.model_name)

        with engine.connect() as db_connection:
            db_model_data = db_connection.execute(select_).mappings().first()
            if db_model_data is not None:
                self._copy_model_data(db_model_data)
                self._load_cell_data_from_db(db_connection)
                self.logger.info(f"Загрузка BI модели завершена")
            else:
                stmt = insert(self.db_table).values(base_voxel_model_id=self.segment_model.voxel_model.id,
                                                    base_segment_model_name=self.segment_model.model_name,
                                                    bi_model_name=self.model_name,
                                                    MSE_data=self.mse_data
                                                    )
                db_connection.execute(stmt)
                db_connection.commit()
                self.id = self._get_last_model_id()
                self._calk_segment_model()
                self._save_cell_data_in_db(db_connection)
                db_connection.commit()
                self.logger.info(f"Расчет BI модели завершен и загружен в БД")

    def _calk_segment_model(self):
        base_scan = ScanDB.get_scan_from_id(self.segment_model.voxel_model.base_scan_id)
        self.__calk_cells_z()
        self.__calk_mse(base_scan)

    def __calk_cells_z(self):
        for cell in self._model_structure.values():
            n_s = self.__get_cell_neighbour_structure(cell)
            cell.left_down["Z"], cell.left_down["MSE"] = self.__calk_mean_z([[n_s[0][0], n_s[0][1]],
                                                                             [n_s[1][0], n_s[1][1]]])
            cell.left_up["Z"], cell.left_up["MSE"] = self.__calk_mean_z([[n_s[0][1], n_s[0][2]],
                                                                         [n_s[1][1], n_s[1][2]]])
            cell.right_down["Z"], cell.right_down["MSE"] = self.__calk_mean_z([[n_s[1][0], n_s[1][1]],
                                                                               [n_s[2][0], n_s[2][1]]])
            cell.right_up["Z"], cell.right_up["MSE"] = self.__calk_mean_z([[n_s[1][1], n_s[1][2]],
                                                                           [n_s[2][1], n_s[2][2]]])
        self.logger.info(f"Расчет средних высот завершен")

    @staticmethod
    def __calk_mean_z(n_s):
        z, mse = [], []
        if n_s[0][0] is not None:
            z.append(n_s[0][0].cell.get_z_from_xy(n_s[0][0].voxel.X + n_s[0][0].voxel.step,
                                                  n_s[0][0].voxel.Y + n_s[0][0].voxel.step))
            mse.append(n_s[0][0].cell.mse)
        if n_s[0][1] is not None:
            z.append(n_s[0][1].cell.get_z_from_xy(n_s[0][1].voxel.X + n_s[0][1].voxel.step,
                                                  n_s[0][1].voxel.Y))
            mse.append(n_s[0][1].cell.mse)
        if n_s[1][0] is not None:
            z.append(n_s[1][0].cell.get_z_from_xy(n_s[1][0].voxel.X,
                                                  n_s[1][0].voxel.Y + n_s[1][0].voxel.step))
            mse.append(n_s[1][0].cell.mse)
        if n_s[1][1] is not None:
            z.append(n_s[1][1].cell.get_z_from_xy(n_s[1][1].voxel.X,
                                                  n_s[1][1].voxel.Y))
            mse.append(n_s[1][1].cell.mse)
        sum_p = 0
        sum_of_pz = None
        for idx, mse in enumerate(mse):
            if mse is None:
                continue
            p = 1 / (mse ** 2)
            try:
                sum_of_pz += p * z[idx]
            except TypeError:
                sum_of_pz = p * z[idx]
            sum_p += p
        try:
            avr_z = sum_of_pz / sum_p
            mse = 1 / (sum_p ** 0.5)
        except TypeError:
            avr_z = None
            mse = None
        return avr_z, mse

    def __get_cell_neighbour_structure(self, cell):
        step = cell.voxel.step
        x0, y0 = cell.voxel.X + step / 2, cell.voxel.Y + step / 2
        neighbour_structure = [[(-step, -step), (-step, 0), (-step, step)],
                               [(0, -step), (0, 0), (0, step)],
                               [(step, -step), (step, 0), (step, step)]]
        for x in range(3):
            for y in range(3):
                dx, dy = neighbour_structure[x][y]
                point = Point(X=x0 + dx, Y=y0 + dy, Z=0, R=0, G=0, B=0)
                try:
                    cell = self.get_model_element_for_point(point)
                    neighbour_structure[x][y] = cell
                except KeyError:
                    neighbour_structure[x][y] = None
        return neighbour_structure

    def __calk_mse(self, base_scan):
        for point in base_scan:
            try:
                cell = self.get_model_element_for_point(point)
                cell_z = cell.get_z_from_xy(point.X, point.Y)
            except AttributeError:
                continue
            try:
                cell.vv += (point.Z - cell_z) ** 2
            except AttributeError:
                cell.vv = (point.Z - cell_z) ** 2
        for cell in self._model_structure.values():
            if len(cell.voxel) <= 4:
                cell.mse = None
            else:
                try:
                    cell.mse = (cell.vv / (len(cell.voxel) - 4)) ** 0.5
                except AttributeError:
                    cell.mse = None
        self.logger.info(f"Расчет СКП высот завершен")

    def _copy_model_data(self, db_model_data: dict):
        self.id = db_model_data["id"]
        self.base_voxel_model_id = db_model_data["base_voxel_model_id"]
        self.base_segment_model_name = db_model_data["base_segment_model_name"]
        self.model_name = db_model_data["bi_model_name"]
        self.mse_data = db_model_data["MSE_data"]

    def _create_model_structure(self, element_class):
        for cell in self.segment_model:
            try:
                voxel = cell.voxel
            except AttributeError:
                continue
            model_key = f"{voxel.X:.5f}_{voxel.Y:.5f}_{voxel.Z:.5f}"
            self._model_structure[model_key] = element_class(cell, self)
