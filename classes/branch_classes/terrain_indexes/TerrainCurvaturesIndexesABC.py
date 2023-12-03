from abc import abstractmethod

import numpy as np

from classes.DemModelDB import DemModelDB
from classes.Polynomial2ModelDB import Polynomial2ModelDB
from classes.branch_classes.terrain_indexes.DEMIndexABC import DEMIndexABC


class TerrainCurvaturesIndexesABC(DEMIndexABC):

    def __init__(self, dem_model, abs_value=True, full_neighbours=False):
        self.params = None
        self.curvature_index = None
        self.len = 9
        self.abs_value = abs_value
        super().__init__(dem_model, full_neighbours)

    def __get_A_Z_matrix(self, cell_neighbour_structure):
        s = self.dem_model.voxel_model.step
        A, Z = [], []
        for i in range(len(cell_neighbour_structure)):
            for j in range(len(cell_neighbour_structure[0])):
                cell = cell_neighbour_structure[i][j]
                if cell is None:
                    continue
                x = -s + s * j
                y = -s + s * i
                A.append([x ** 2, y ** 2, x * y, x, y, 1])
                Z.append(cell)
        A = np.array(A)
        Z = np.array(Z)
        return A, Z

    @staticmethod
    def __calc_paraboloid_params(A, Z):
        try:
            N = A.T @ A
            N_inv = np.linalg.inv(N)
            T = N_inv @ A.T @ Z
            params = {"A": T[0], "B": T[1], "C": T[2],
                      "D": T[3], "E": T[4], "F": T[5]}
            return params
        except np.linalg.LinAlgError:
            return None

    @abstractmethod
    def _calc_curvature_index(self):
        pass

    @abstractmethod
    def _get_result(self):
        pass

    def _get_cell_neighbour_structure(self, cell):
        """
        Создает структуру соседних ячеек относительно ячейки cell
        :param cell: чентральная ячейка относительно которой ищутся соседи
        :return: 3х3 масив с ячейками относительно ячейки cell
        """
        # if isinstance(self.dem_model, DemModelDB):
        #     return super()._get_cell_neighbour_structure(cell)
        if isinstance(self.dem_model, Polynomial2ModelDB):
            neighbour_structure = [[None, None, None],
                                   [None, cell, None],
                                   [None, None, None]]
            return neighbour_structure
        return super()._get_cell_neighbour_structure(cell)

    def _do_prepare_actions(self, cell_neighbour_structure):
        # if isinstance(self.dem_model, DemModelDB):
        #     self.A, self.Z = self.__get_A_Z_matrix(cell_neighbour_structure)
        #     self.params = self.__calc_paraboloid_params(self.A, self.Z)
        #     self.len = len(self.A)
        #     return
        if isinstance(self.dem_model, Polynomial2ModelDB):
            cell = cell_neighbour_structure[1][1]
            self.full_neighbours = False
            self.params = {"A": cell.a, "B": cell.b, "C": cell.c,
                           "D": cell.d, "E": cell.e, "F": cell.f}
            return
        self.A, self.Z = self.__get_A_Z_matrix(cell_neighbour_structure)
        self.params = self.__calc_paraboloid_params(self.A, self.Z)
        self.len = len(self.A)

    def calk_index_value(self, cell_neighbour_structure):
        self._do_prepare_actions(cell_neighbour_structure)
        if self.params is None:
            return None
        if self.full_neighbours is False or self.len == 9:
            self._calc_curvature_index()
            result = self._get_result()
            return abs(result) if self.abs_value else result


class MeanCurvatureIndex(TerrainCurvaturesIndexesABC):
    def __init__(self, dem_model, abs_value=True, full_neighbours=False):
        super().__init__(dem_model, abs_value, full_neighbours)
        self.index_name = "Mean_Curvature_Index"

    def _calc_curvature_index(self):
        self.curvature_index = -self.params["A"] - self.params["B"]

    def _get_result(self):
        return self.curvature_index


class MaxAbsCurvatureIndex(TerrainCurvaturesIndexesABC):

    def __init__(self, dem_model, abs_value=True, full_neighbours=False):
        super().__init__(dem_model, abs_value, full_neighbours)
        self.index_name = "Max_Abs_Curvature_Index"

    def _calc_curvature_index(self):
        self.curvature_max = -self.params["A"] - self.params["B"] + \
                             ((self.params["A"] - self.params["B"]) ** 2 + self.params["C"] ** 2) ** 0.5
        self.curvature_min = -self.params["A"] - self.params["B"] - \
                             ((self.params["A"] - self.params["B"]) ** 2 + self.params["C"] ** 2) ** 0.5

    def _get_result(self):
        curvature = self.curvature_max \
            if abs(self.curvature_min) < abs(self.curvature_max) \
            else self.curvature_min
        return curvature


class ProfileCurvatureIndex(TerrainCurvaturesIndexesABC):
    def __init__(self, dem_model, abs_value=True, full_neighbours=False):
        super().__init__(dem_model, abs_value, full_neighbours)
        self.index_name = "Profile_Curvature_Index"

    def _calc_curvature_index(self):
        self.prof_c = (-200 * (self.params["A"] * self.params["D"] ** 2 +
                               self.params["B"] * self.params["E"] ** 2 +
                               self.params["C"] * self.params["D"] * self.params["E"])) / \
                      ((self.params["E"] ** 2 + self.params["D"] ** 2) *
                       (1 + self.params["E"] ** 2 + self.params["D"] ** 2) ** 1.5)

    def _get_result(self):
        return self.prof_c


class PlaneCurvatureIndex(TerrainCurvaturesIndexesABC):
    def __init__(self, dem_model, abs_value=True, full_neighbours=False):
        super().__init__(dem_model, abs_value, full_neighbours)
        self.index_name = "Plane_Curvature_Index"

    def _calc_curvature_index(self):
        self.plan_c = (200 * (self.params["B"] * self.params["D"] ** 2 +
                              self.params["A"] * self.params["E"] ** 2 +
                              self.params["C"] * self.params["D"] * self.params["E"])) / \
                      ((self.params["E"] ** 2 + self.params["D"] ** 2) ** 1.5)

    def _get_result(self):
        return self.plan_c


class SlopeXIndex(TerrainCurvaturesIndexesABC):
    def __init__(self, dem_model, abs_value=True, full_neighbours=False):
        super().__init__(dem_model, abs_value, full_neighbours)
        self.index_name = "Slope_X_Index"

    def _calc_curvature_index(self):
        self.slope_x = self.params["D"]

    def _get_result(self):
        return self.slope_x


class SlopeYIndex(TerrainCurvaturesIndexesABC):
    def __init__(self, dem_model, abs_value=True, full_neighbours=False):
        super().__init__(dem_model, abs_value, full_neighbours)
        self.index_name = "Slope_Y_Index"

    def _calc_curvature_index(self):
        self.slope_y = self.params["E"]

    def _get_result(self):
        return self.slope_y


class SlopeFullIndex(TerrainCurvaturesIndexesABC):
    def __init__(self, dem_model, abs_value=True, full_neighbours=False, in_degrees=True):
        self.in_degrees = in_degrees
        super().__init__(dem_model, abs_value, full_neighbours)
        self.index_name = "Slope_Full_Index"

    def _calc_curvature_index(self):
        from math import atan
        self.slope_full = atan((self.params["E"] ** 2 + self.params["E"] ** 2) ** 0.5)

    def _get_result(self):
        from math import degrees
        result = degrees(self.slope_full) if self.in_degrees else self.slope_full
        return result
