import logging
from abc import ABC, abstractmethod

from sqlalchemy import select, desc, update

from CONFIG import LOGGER
from utils.segmented_mdl_utils.segmented_models_plotters.MsePlotterPlotly import MsePlotterPlotly
from utils.segmented_mdl_utils.segmented_models_plotters.SegmentModelPlotly import SegmentModelPlotly
from utils.start_db import engine


class SegmentedModelABC(ABC):

    logger = logging.getLogger(LOGGER)
    db_table = None

    def __init__(self, voxel_model, element_class):
        self.id = None
        self.base_voxel_model_id = voxel_model.id
        self.voxel_model = voxel_model
        self.model_name = None
        self._model_structure = {}
        self._create_model_structure(element_class)

    def __iter__(self):
        return iter(self._model_structure.values())

    def __str__(self):
        return f"{self.__class__.__name__} [ID: {self.id},\tmodel_name: {self.model_name}]"

    def __repr__(self):
        return f"{self.__class__.__name__} [ID: {self.id}]"

    def _create_model_structure(self, element_class):
        for voxel in self.voxel_model:
            model_key = f"{voxel.X:.5f}_{voxel.Y:.5f}_{voxel.Z:.5f}"
            self._model_structure[model_key] = element_class(voxel)

    def get_model_element_for_point(self, point):
        X = point.X // self.voxel_model.step * self.voxel_model.step
        Y = point.Y // self.voxel_model.step * self.voxel_model.step
        if self.voxel_model.is_2d_vxl_mdl is False:
            Z = point.Z // self.voxel_model.step * self.voxel_model.step
        else:
            Z = self.voxel_model.min_Z
        model_key = f"{X:.5f}_{Y:.5f}_{Z:.5f}"
        return self._model_structure.get(model_key, None)

    def _calk_model_mse(self, db_connection):
        vv = 0
        sum_of_r = 0
        for cell in self:
            if cell.r > 0 and cell.mse is not None:
                vv += (cell.mse ** 2) * cell.r
                sum_of_r += cell.r
        try:
            self.mse_data = (vv / sum_of_r) ** 0.5
        except ZeroDivisionError:
            self.mse_data = None
        stmt = update(self.db_table).values(MSE_data=self.mse_data).where(self.db_table.c.id == self.id)
        db_connection.execute(stmt)
        db_connection.commit()
        self.logger.info(f"Расчет СКП модели завершен и загружен в БД")

    @abstractmethod
    def _calk_segment_model(self):
        pass

    def plot(self, plotter=SegmentModelPlotly()):
        plotter.plot(self)

    def plot_mse(self, plotter=MsePlotterPlotly()):
        plotter.plot(self)

    @abstractmethod
    def _copy_model_data(self, db_model_data: dict):
        pass

    def _load_cell_data_from_db(self, db_connection):
        for cell in self._model_structure.values():
            cell._load_cell_data_from_db(db_connection)

    def _save_cell_data_in_db(self, db_connection):
        for cell in self._model_structure.values():
            cell._save_cell_data_in_db(db_connection)

    def _get_last_model_id(self):
        """
        Возвращает последний id для точки в таблице БД points
        :return: последний id для точки в таблице БД points
        """
        with engine.connect() as db_connection:
            stmt = (select(self.db_table.c.id).order_by(desc("id")))
            last_model_id = db_connection.execute(stmt).first()
            if last_model_id:
                return last_model_id[0]
            else:
                return 0
