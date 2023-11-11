from classes.branch_classes.terrain_indexes.MeanAbsCurvatureIndex import MeanAbsCurvatureIndex


class ProfileCurvatureAbsIndex(MeanAbsCurvatureIndex):

    def calk_index_value(self, cell_neighbour_structure):
        A, Z = self._get_A_Z_matrix(cell_neighbour_structure)
        params = self._calc_paraboloid_params(A, Z)
        if params is None:
            return None
        if self.full_neighbours is False or len(A) == 9:
            prof_c = (-200 * (params["A"] * params["D"] ** 2 +
                              params["B"] * params["E"] ** 2 +
                              params["C"] * params["D"] * params["E"])) / \
                             ((params["E"] ** 2 + params["D"] ** 2) *
                              (1 + params["E"] ** 2 + params["D"] ** 2) ** 1.5)
            return abs(prof_c)


class PlaneCurvatureAbsIndex(MeanAbsCurvatureIndex):
    def calk_index_value(self, cell_neighbour_structure):
        A, Z = self._get_A_Z_matrix(cell_neighbour_structure)
        params = self._calc_paraboloid_params(A, Z)
        if params is None:
            return None
        if self.full_neighbours is False or len(A) == 9:
            plan_c = (200 * (params["B"] * params["D"] ** 2 +
                             params["A"] * params["E"] ** 2 +
                             params["C"] * params["D"] * params["E"])) / \
                            ((params["E"] ** 2 + params["D"] ** 2) ** 1.5)
            return abs(plan_c)
