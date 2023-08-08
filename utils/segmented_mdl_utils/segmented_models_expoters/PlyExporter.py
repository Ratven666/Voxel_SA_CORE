from os import path

from utils.segmented_mdl_utils.segmented_models_expoters.ExporterABC import ExporterABC


class PlyExporter(ExporterABC):

    def __init__(self, segmented_model, grid_densification=1):
        super().__init__(segmented_model, grid_densification)

    def __create_header(self):
        return f"ply\n" \
               f"format ascii 1.0\n" \
               f"comment author: Greg Turk\n" \
               f"comment object: another cube\n" \
               f"element vertex {len(self.triangulation.vertices)}\n" \
               f"property float x\n" \
               f"property float y\n" \
               f"property float z\n" \
               f"property uchar red\n" \
               f"property uchar green\n" \
               f"property uchar blue\n" \
               f"element face {len(self.triangulation.faces)}\n" \
               f"property list uchar int vertex_index\n" \
               f"end_header\n"

    def __create_vertices_str(self):
        vertices_str = ""
        for point in self.scan:
            vertices_str += f"{point.X} {point.Y} {point.Z} {point.R} {point.G} {point.B}\n"
        return vertices_str

    def __create_faces_str(self):
        faces_str = ""
        for face in self.triangulation.faces:
            faces_str += f"3 {face[0]} {face[1]} {face[2]}\n"
        return faces_str

    def __save_ply(self, file_path):
        with open(file_path, "wb") as file:
            file.write(self.__create_header().encode("ascii"))
            file.write(self.__create_vertices_str().encode("ascii"))
            file.write(self.__create_faces_str().encode("ascii"))

    def export(self, file_path="."):
        self.do_base_calculation()
        file_path = path.join(file_path, f"{self.scan.scan_name.replace(':', '=')}.ply")
        self.__save_ply(file_path)
