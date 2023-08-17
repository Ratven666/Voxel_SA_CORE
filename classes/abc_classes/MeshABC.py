from utils.mesh_utils.mesh_triangulators.ScipyTriangulator import ScipyTriangulator


class MeshABC:

    def __init__(self, scan, scan_triangulator=ScipyTriangulator):
        self.scan = scan
        self.scan_triangulator = scan_triangulator
        self.mesh_name = self.__name_generator()
        self.len = 0

    def __name_generator(self):
        return f"MESH_{self.scan.scan_name}"
