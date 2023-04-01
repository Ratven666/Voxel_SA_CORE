import logging
from abc import ABC, abstractmethod

from CONFIG import LOGGER
from utils.segmented_mdl_utils.segmented_models_iterators.SegmentedModelFilteredByVoxelLenIterator import \
    SegmentedModelFilteredByVoxelLenIterator


class SegmentedModelABC(ABC):

    logger = logging.getLogger(LOGGER)

    def __init__(self, voxel_model, element_class, min_voxel_len=0):
        self.voxel_model = voxel_model
        self._model_structure = {}
        self.min_voxel_len = min_voxel_len
        self.__create_model_structure(element_class)

    def __iter__(self):
        return SegmentedModelFilteredByVoxelLenIterator(self)

    def __create_model_structure(self, element_class):
        for voxel in self.voxel_model:
            model_key = f"{voxel.X}_{voxel.Y}_{voxel.Z}"
            self._model_structure[model_key] = element_class(voxel)

    def get_model_element_for_point(self, point):
        X = point.X // self.voxel_model.step * self.voxel_model.step
        Y = point.Y // self.voxel_model.step * self.voxel_model.step
        if self.voxel_model.is_2d_vxl_mdl is False:
            Z = point.Z // self.voxel_model.step * self.voxel_model.step
        else:
            Z = self.voxel_model.min_Z
        model_key = f"{X}_{Y}_{Z}"
        return self._model_structure[model_key]

    @abstractmethod
    def _calk_segment_model(self):
        pass

    @abstractmethod
    def plot(self, plotter):
        pass

    @abstractmethod
    def _copy_model_data(self, db_model_data: dict):
        pass

    def _load_cell_data_from_db(self, db_connection):
        for cell in self._model_structure.values():
            cell._load_cell_data_from_db(db_connection)

    def _save_cell_data_in_db(self, db_connection):
        for cell in self._model_structure.values():
            cell._save_cell_data_in_db(db_connection)
