from os import path

import ezdxf

from classes.Point import Point
from classes.ScanLite import ScanLite
from utils.scan_utils.ScanTriangulator import ScanTriangulator


class DxfExporter:

    def __init__(self, segmented_model, grid_densification=1):
        self.segmented_model = segmented_model
        self.grid_densification = grid_densification

    def _get_next_point_on_grid(self):
        x_count, y_count = [count * self.grid_densification + 1 for count
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

    @staticmethod
    def __save_dxf(triangulation, file_path):
        doc = ezdxf.new("R2000")
        msp = doc.modelspace()
        mesh = msp.add_mesh()
        mesh.dxf.subdivision_levels = 0
        with mesh.edit_data() as mesh_data:
            mesh_data.vertices = triangulation.vertices
            mesh_data.faces = triangulation.faces
        doc.saveas(file_path)

    def export(self, file_path="."):
        scan = ScanLite(f"Mesh_{self.segmented_model.model_name}_step="
                        f"{self.segmented_model.voxel_model.step / self.grid_densification}")
        for point in self._get_next_point_on_grid():
            scan.add_point(point)
        triangulation = ScanTriangulator(scan)
        file_path = path.join(file_path, f"{scan.scan_name.replace(':', '=')}.dxf")
        self.__save_dxf(triangulation, file_path)

        # doc = ezdxf.new("R2000")
        # msp = doc.modelspace()
        # mesh = msp.add_mesh()
        # # do not subdivide cube, 0 is the default value
        # mesh.dxf.subdivision_levels = 0
        # with mesh.edit_data() as mesh_data:
        #     mesh_data.vertices = triangulation.vertices
        #     mesh_data.faces = triangulation.faces
        # doc.saveas(path.join(file_path, f"{scan.scan_name.replace(':', '=')}.dxf"))
