import logging

from sqlalchemy import select

from CONFIG import LOGGER
from classes.MeshDB import MeshDB
from classes.MeshLite import MeshLite
from classes.MeshSegmentModelDB import MeshSegmentModelDB
from classes.Point import Point
from classes.ScanLite import ScanLite
from classes.Triangle import Triangle
from classes.VoxelModelDB import VoxelModelDB
from utils.mesh_utils.mesh_plotters.MeshPlotterPlotly import MeshPlotterPlotly
from utils.scan_utils.scan_samplers.VoxelDownsamplingScanSampler import VoxelDownsamplingScanSampler
from utils.start_db import Tables, engine


class MeshMSEConst:
    logger = logging.getLogger(LOGGER)
    db_table = Tables.meshes_db_table

    def __init__(self, scan, max_border_length_m, max_triangle_mse_m, n=5, is_2d=True, delete_temp_models=True):
        self.scan = scan
        self.mesh = None
        self.sampled_scan = None
        self.max_border_length = max_border_length_m
        self.max_triangle_mse = max_triangle_mse_m
        self.n = n
        self.is_2d = is_2d
        self.delete_temp_models = delete_temp_models
        self.last_triangle_id = None
        self.mesh_name = self.__name_generator()
        self.triangles = {}
        self.temp_scans_id = []
        self.__init_mesh()

    def __iter__(self):
        return iter(self.mesh)

    def __len__(self):
        return len(self.mesh)

    def plot(self, plotter=MeshPlotterPlotly()):
        """
        Вывод отображения скана
        :param plotter: объект определяющий логику отображения поверхности
        :return: None
        """
        plotter.max_mse = self.max_triangle_mse
        plotter.plot(self.mesh)

    def __name_generator(self):
        d_type = "2D" if self.is_2d else "3D"
        return (f"MESH_{self.scan.scan_name}"
                f"_max_brd_{self.max_border_length}"
                f"_max_mse_{self.max_triangle_mse}_n_{self.n}_{d_type}")

    def __init_mesh(self):
        select_ = select(self.db_table).where(self.db_table.c.mesh_name == self.mesh_name)
        with engine.connect() as db_connection:
            db_mesh_data = db_connection.execute(select_).mappings().first()
            if db_mesh_data is not None:
                mesh_id = db_mesh_data["id"]
                self.mesh = MeshDB.get_mesh_by_id(mesh_id)
            else:
                self.__calculate_mesh()
                self.__init_mesh()

    # def __calculate_mesh(self):
    #     self.__do_preliminary_calculations()
    #     for _ in range(self.n):
    #         self.mesh = MeshLite(self.__get_mesh_scan())
    #         self.mesh.calk_mesh_mse(self.sampled_scan)
    #         self.__find_and_prepare_bad_triangles()
    #         if len(self.mesh) == 0:
    #             break
    #         self.__calc_new_and_replace_bad_triangles()
    #     self.mesh = MeshLite(self.__get_mesh_scan())
    #     self.mesh.calk_mesh_mse(self.scan)
    #     self.__save_result_mesh()

    def __calculate_mesh(self):
        self.sampled_scan = VoxelDownsamplingScanSampler(grid_step=self.max_border_length,
                                                         is_2d_sampling=self.is_2d,
                                                         average_the_data=False).do_sampling(self.scan)
        for _ in range(self.n):
            self.mesh = MeshLite(self.sampled_scan)
            self.mesh.calk_mesh_mse(self.scan, delete_temp_models=True)
            self.__find_and_prepare_bad_triangles()

        self.sampled_scan.scan_name = self.mesh_name[5:]
        self.sampled_scan.save_to_db()
        self.mesh = MeshDB(self.sampled_scan)
        self.mesh.calk_mesh_mse(self.scan, delete_temp_models=True)






            # for _ in range(self.n):
            #     self.__find_and_prepare_bad_triangles()
            #     if len(self.mesh) == 0:
            #         break
            #     self.__calc_new_and_replace_bad_triangles()
            #     self.mesh = MeshLite(self.__get_mesh_scan())
            #     self.mesh.calk_mesh_mse(self.scan)


        # self.mesh = MeshLite(self.__get_mesh_scan())
        # self.mesh.calk_mesh_mse(self.scan)
        # self.__save_result_mesh()

    # def __do_preliminary_calculations(self):
    #     self.sampled_scan = VoxelDownsamplingScanSampler(grid_step=self.max_border_length,
    #                                                      is_2d_sampling=self.is_2d,
    #                                                      average_the_data=False).do_sampling(self.scan)
    #     self.mesh = MeshLite(self.sampled_scan)
    #     self.mesh.calk_mesh_mse(self.scan)
    #     for triangle in self.mesh:
    #         self.triangles[triangle.id] = triangle
    #     self.last_triangle_id = min(self.triangles)
    #     self.sampled_scan = self.scan

    @staticmethod
    def __calc_centroid_point_in_triangle(triangle):
        s_x, s_y, s_z = 0, 0, 0
        for point in triangle:
            s_x += point.X
            s_y += point.Y
            s_z += point.Z
        return Point(X=s_x / 3, Y=s_y / 3, Z=s_z / 3,
                     R=0, G=0, B=0)

    # def __find_and_prepare_bad_triangles(self):
    #     bad_triangles = []
    #     for triangle in self.mesh:
    #         if triangle.mse is None:
    #             continue
    #         if triangle.mse > self.max_triangle_mse:
    #             triangle.container_dict["centroid_point"] = self.__calc_centroid_point_in_triangle(triangle)
    #             triangle.container_dict["dist"] = float("inf")
    #             triangle.container_dict["c_point"] = None
    #             bad_triangles.append(triangle)
    #     self.mesh.triangles = bad_triangles
    #     self.__calc_mesh_triangles_centroids()

    def __find_and_prepare_bad_triangles(self):
        bad_triangles = []
        for triangle in self.mesh:
            if triangle.mse is None:
                continue
            if triangle.mse > self.max_triangle_mse:
                triangle.container_dict["centroid_point"] = self.__calc_centroid_point_in_triangle(triangle)
                triangle.container_dict["dist"] = float("inf")
                triangle.container_dict["c_point"] = None
                bad_triangles.append(triangle)
        self.mesh.triangles = bad_triangles
        self.__calc_mesh_triangles_centroids()

    def __get_mesh_vm_and_sm_models(self):
        area = ((self.sampled_scan.max_X - self.sampled_scan.min_X) *
                (self.sampled_scan.max_Y - self.sampled_scan.min_Y))
        voxel_size = area / self.sampled_scan.len
        voxel_size = round((voxel_size // 0.05 + 1) * 0.05, 2)
        if voxel_size > 25:
            voxel_size = 25
        # vm = VoxelModelDB(self.sampled_scan, voxel_size, is_2d_vxl_mdl=True)
        vm = VoxelModelDB(self.scan, voxel_size, is_2d_vxl_mdl=True)
        mesh_segment_model = MeshSegmentModelDB(vm, self.mesh)
        return vm, mesh_segment_model

    # def __calc_mesh_triangles_centroids(self):
    #     temp_scan = ScanLite("Temp_scan")
    #     triangles = {}
    #     vm, m_sm = self.__get_mesh_vm_and_sm_models()
    #     for point in self.sampled_scan:
    #     # for point in self.scan:
    #         cell = m_sm.get_model_element_for_point(point)
    #         if cell is None or len(cell.triangles) == 0:
    #             continue
    #         for triangle in cell.triangles:
    #         # for triangle in self.mesh:
    #             if triangle.is_point_in_triangle(point):
    #                 temp_scan.add_point(point)
    #                 if triangle.id not in triangles:
    #                     triangles[triangle.id] = triangle
    #                 # triangle = triangles[triangle.id]
    #                 # c_p = self.__calc_centroid_point_in_triangle(triangle)
    #                 dist = ((point.X - triangle.container_dict["centroid_point"].X) ** 2 +
    #                         (point.Y - triangle.container_dict["centroid_point"].Y) ** 2) ** 0.5
    #
    #                 if dist < triangle.container_dict["dist"]:
    #                     triangle.container_dict["dist"] = dist
    #                     triangle.container_dict["c_point"] = point
    #                 # triangles[triangle.id] = triangle
    #                 break
    #     self.mesh.triangles = triangles.values()
    #     self.sampled_scan = temp_scan
    #     if self.delete_temp_models:
    #         vm.delete_model()
    #         m_sm.delete_model()

    def __calc_mesh_triangles_centroids(self):
        triangles = {}
        vm, m_sm = self.__get_mesh_vm_and_sm_models()
        # for point in self.sampled_scan:
        for point in self.scan:
            cell = m_sm.get_model_element_for_point(point)
            if cell is None or len(cell.triangles) == 0:
                continue
            for triangle in cell.triangles:
            # for triangle in self.mesh:
                if triangle.is_point_in_triangle(point):
                    if triangle.id not in triangles:
                        triangles[triangle.id] = triangle
                    dist = ((point.X - triangle.container_dict["centroid_point"].X) ** 2 +
                            (point.Y - triangle.container_dict["centroid_point"].Y) ** 2) ** 0.5

                    if dist < triangle.container_dict["dist"]:
                        triangle.container_dict["dist"] = dist
                        triangle.container_dict["c_point"] = point
                    break
        for triangle in triangles.values():
            # print(triangle)
            self.sampled_scan.add_point(triangle.container_dict["c_point"])
        vm.delete_model()
        m_sm.delete_model()

    # def __split_triangle(self, triangle):
    #     self.last_triangle_id -= 1
    #     t_1 = Triangle(triangle.point_0, triangle.point_1,
    #                    triangle.container_dict["c_point"], id_=self.last_triangle_id)
    #     self.last_triangle_id -= 1
    #     t_2 = Triangle(triangle.point_1, triangle.point_2,
    #                    triangle.container_dict["c_point"], id_=self.last_triangle_id)
    #     self.last_triangle_id -= 1
    #     t_3 = Triangle(triangle.point_2, triangle.point_0,
    #                    triangle.container_dict["c_point"], id_=self.last_triangle_id)
    #     return [t_1, t_2, t_3]

    # def __calc_new_and_replace_bad_triangles(self):
    #     bad_triangles = []
    #     new_triangles = []
    #     for triangle in self.mesh:
    #         bad_triangles.append(triangle)
    #         new_triangles += self.__split_triangle(triangle)
    #     self.mesh.triangles = new_triangles
    #     #############
    #     # self.sampled_scan = self.sampled_scan.save_to_db()
    #     # self.temp_scans_id.append(self.sampled_scan.id)
    #     # #############
    #     # self.mesh.calk_mesh_mse(self.sampled_scan, clear_previous_mse=True,
    #     #                         delete_temp_models=self.delete_temp_models)
    #     for triangle in bad_triangles:
    #         self.triangles.pop(triangle.id)
    #     for triangle in new_triangles:
    #         self.triangles[triangle.id] = triangle

    # def __get_mesh_scan(self):
    #     points = {}
    #     for triangle in self.triangles.values():
    #         for point in triangle:
    #             if point.id in points:
    #                 continue
    #             points[point.id] = point
    #     scan = ScanLite(self.mesh_name[5:])
    #     for point in points.values():
    #         scan.add_point(point)
    #     scan = scan.save_to_db()
    #     return scan

    # def __save_result_mesh(self):
    #     self.mesh.scan = self.__get_mesh_scan()
    #     self.mesh.mesh_name = self.mesh_name
    #     self.mesh.triangles = list(self.triangles.values())
    #     self.mesh.len = len(self.mesh.triangles)
    #     s_r, s_vv = 0, 0
    #     for triangle in self.mesh:
    #         try:
    #             s_vv += triangle.r * triangle.mse ** 2
    #             s_r += triangle.r
    #         except TypeError:
    #             continue
    #     self.mesh.mse = (s_vv / s_r) ** 0.5
    #     self.mesh.r = s_r
    #     self.mesh.save_to_db()

    # def __save_result_mesh(self):
    #     self.mesh.scan = self.__get_mesh_scan()
    #     self.mesh.mesh_name = self.mesh_name
    #     self.mesh.triangles = list(self.triangles.values())
    #     self.mesh.len = len(self.mesh.triangles)
    #     s_r, s_vv = 0, 0
    #     for triangle in self.mesh:
    #         try:
    #             s_vv += triangle.r * triangle.mse ** 2
    #             s_r += triangle.r
    #         except TypeError:
    #             continue
    #     self.mesh.mse = (s_vv / s_r) ** 0.5
    #     self.mesh.r = s_r
    #     self.mesh.save_to_db()
