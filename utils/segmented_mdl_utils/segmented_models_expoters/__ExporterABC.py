from abc import ABC, abstractmethod

from classes.Point import Point
from classes.ScanLite import ScanLite
from utils.scan_utils.scan_triangulators.__ScanTriangulator import ScanTriangulator
from utils.scan_utils.scan_triangulators.mesh_filters.__MaxEdgeLengthFilter import MaxEdgeLengthFilter


class ExporterABC(ABC):

    def __init__(self, segmented_model,
                 grid_densification,
                 filtrate,
                 scan_triangelator=ScanTriangulator(filters=[MaxEdgeLengthFilter()])):
        self.segmented_model = segmented_model
        self.grid_densification = grid_densification
        self.filtrate = filtrate
        self.triangulation = scan_triangelator
        self.scan = None

    def _get_next_point_on_grid(self):
        x_count, y_count = [round(count * self.grid_densification + 1) for count
                            in [self.segmented_model.voxel_model.X_count,
                                self.segmented_model.voxel_model.Y_count]]
        z_count = self.segmented_model.voxel_model.Z_count
        step = self.segmented_model.voxel_model.step
        min_x, min_y, min_z = self.segmented_model.voxel_model.min_X, \
                              self.segmented_model.voxel_model.min_Y, \
                              self.segmented_model.voxel_model.min_Z
        for k in range(z_count):
            for i in range(x_count):
                for j in range(y_count):
                    point = Point(X=min_x + i * step / self.grid_densification,
                                  Y=min_y + j * step / self.grid_densification,
                                  Z=min_z + k * step,
                                  R=0, G=0, B=0)
                    z = self.segmented_model.get_z_from_point(point)
                    if z is not None:
                        cell = self.segmented_model.get_model_element_for_point(point)
                        point.Z = round(z, 4)
                        point.R = cell.voxel.R
                        point.G = cell.voxel.G
                        point.B = cell.voxel.B
                        yield point

    def __create_mashed_scan(self):
        self.scan = ScanLite(f"Mesh_{self.segmented_model.model_name}_step="
                             f"{self.segmented_model.voxel_model.step / self.grid_densification}")
        for point in self._get_next_point_on_grid():
            self.scan.add_point(point)

    def __set_max_edge_length(self, max_edge_length):
        for filter_ in self.triangulation.filters:
            if isinstance(filter_, MaxEdgeLengthFilter):
                filter_.max_edge_length = max_edge_length

    def do_base_calculation(self):
        self.__create_mashed_scan()
        self.__set_max_edge_length(self.segmented_model.voxel_model.step * 4)  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.triangulation.triangulate(self.scan, filtrate=self.filtrate)

    @abstractmethod
    def export(self):
        pass
