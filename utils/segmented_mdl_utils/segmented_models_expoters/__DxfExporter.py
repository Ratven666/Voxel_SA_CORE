from os import path

import ezdxf

from utils.segmented_mdl_utils.segmented_models_expoters.__ExporterABC import ExporterABC


class DxfExporter(ExporterABC):

    def __init__(self, segmented_model, grid_densification=1, filtrate=True):
        super().__init__(segmented_model, grid_densification, filtrate)

    def __save_dxf(self, file_path):
        doc = ezdxf.new("R2000")
        msp = doc.modelspace()
        mesh = msp.add_mesh()
        mesh.dxf.subdivision_levels = 0
        with mesh.edit_data() as mesh_data:
            mesh_data.vertices = self.triangulation.vertices
            mesh_data.faces = self.triangulation.faces
        doc.saveas(file_path)

    def export(self, file_path="."):
        self.do_base_calculation()
        file_path = path.join(file_path, f"{self.scan.scan_name.replace(':', '=')}.dxf")
        self.__save_dxf(file_path)
