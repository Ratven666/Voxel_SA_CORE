import logging
from abc import ABC, abstractmethod

from CONFIG import LOGGER


class SegmentedModelABC(ABC):

    logger = logging.getLogger(LOGGER)

    def __init__(self, voxel_model, element_class):
        self.voxel_model = voxel_model
        self._model_structure = {}
        self.__create_model_structure(element_class)

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
