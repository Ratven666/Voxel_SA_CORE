from classes.Point import Point
from classes.Triangle import Triangle
from classes.abc_classes.MeshABC import MeshABC
from utils.mesh_utils.mesh_triangulators.ScipyTriangulator import ScipyTriangulator


class MeshLite(MeshABC):

    def __init__(self, scan, scan_triangulator=ScipyTriangulator):
        super().__init__(scan, scan_triangulator)
        self.triangles = []
        self.__init_mesh()

    def __iter__(self):
        return iter(self.triangles)

    def __init_mesh(self):
        triangulation = self.scan_triangulator(self.scan).triangulate()
        self.len = len(triangulation.faces)
        for face in triangulation.faces:
            points = []
            for point_idx in face:
                point = Point(id_=triangulation.points_id[point_idx],
                              X=triangulation.vertices[point_idx][0],
                              Y=triangulation.vertices[point_idx][1],
                              Z=triangulation.vertices[point_idx][2],
                              R=triangulation.vertices_colors[point_idx][0],
                              G=triangulation.vertices_colors[point_idx][1],
                              B=triangulation.vertices_colors[point_idx][2])
                points.append(point)
            triangle = Triangle(*points)
            self.triangles.append(triangle)
