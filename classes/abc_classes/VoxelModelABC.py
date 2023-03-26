import logging
from abc import ABC, abstractmethod

from CONFIG import LOGGER
from classes.abc_classes.ScanABC import ScanABC
from utils.voxel_utils.voxel_model_plotters.Voxel_model_plotter import VoxelModelPlotter


class VoxelModelABC(ABC):
    """Абстрактный класс воксельной модели"""

    logger = logging.getLogger(LOGGER)

    def __init__(self, scan: ScanABC, step, is_2d_vxl_mdl=True):
        self.id = None
        self.is_2d_vxl_mdl = is_2d_vxl_mdl
        self.step = step
        self.vm_name: str = self.__name_generator(scan)
        self.len: int = 0
        self.X_count, self.Y_count, self.Z_count = None, None, None
        self.min_X, self.max_X = None, None
        self.min_Y, self.max_Y = None, None
        self.min_Z, self.max_Z = None, None
        self.base_scan_id = None


    def __name_generator(self, scan):
        vm_type = "2D" if self.is_2d_vxl_mdl else "3D"
        return f"VM_{vm_type}_Sc:{scan.scan_name}_st:{self.step}"

    def __str__(self):
        return f"{self.__class__.__name__} " \
               f"[id: {self.id},\tName: {self.vm_name}\tLEN: (x:{self.X_count} * y:{self.Y_count} *" \
               f" z:{self.Z_count})={self.len}]"

    def __repr__(self):
        return f"{self.__class__.__name__} [ID: {self.id}]"

    def __len__(self):
        return self.len

    @abstractmethod
    def __iter__(self):
        pass

    def plot(self, plotter=VoxelModelPlotter()):
        plotter.plot(self)
