from classes.branch_classes.terrain_indexes.MeanAbsCurvatureIndex import MeanAbsCurvatureIndex


class MaxAbsCurvatureIndex(MeanAbsCurvatureIndex):

    def calk_index_value(self, cell_neighbour_structure):
        A, Z = self._get_A_Z_matrix(cell_neighbour_structure)
        params = self._calc_paraboloid_params(A, Z)
        if params is None:
            return None
        if self.full_neighbours is False or len(A) == 9:
            curvature_max = -params["A"] - params["B"] + \
                            ((params["A"] - params["B"]) ** 2 + params["C"] ** 2) ** 0.5
            curvature_min = -params["A"] - params["B"] - \
                            ((params["A"] - params["B"]) ** 2 + params["C"] ** 2) ** 0.5
            curvature = max(abs(curvature_min), abs(curvature_max))
            return curvature
