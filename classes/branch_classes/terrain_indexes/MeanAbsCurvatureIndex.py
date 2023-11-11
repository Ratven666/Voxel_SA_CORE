import numpy as np

from classes.branch_classes.terrain_indexes.DEMIndexABC import DEMIndexABC


class MeanAbsCurvatureIndex(DEMIndexABC):

    def __init__(self, dem_model, full_neighbours=False):
        super().__init__(dem_model, full_neighbours)

    def _get_A_Z_matrix(self, cell_neighbour_structure):
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
    def _calc_paraboloid_params(A, Z):
        try:
            N = A.T @ A
            N_inv = np.linalg.inv(N)
            T = N_inv @ A.T @ Z
            params = {"A": T[0], "B": T[1], "C": T[2],
                      "D": T[3], "E": T[4], "F": T[5]}
            return params
        except np.linalg.LinAlgError:
            return None

    def calk_index_value(self, cell_neighbour_structure):
        A, Z = self._get_A_Z_matrix(cell_neighbour_structure)
        params = self._calc_paraboloid_params(A, Z)
        if params is None:
            return None
        if self.full_neighbours is False or len(A) == 9:
            mean_curvature = -params["A"] - params["B"]
            return abs(mean_curvature)
