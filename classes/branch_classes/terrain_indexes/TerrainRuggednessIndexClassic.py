from classes.branch_classes.terrain_indexes.DEMIndexABC import DEMIndexABC


class TerrainRuggednessIndexClassic(DEMIndexABC):

    def __init__(self, dem_model, full_neighbours=False):
        super().__init__(dem_model, full_neighbours)

    def calk_index_value(self, cell_neighbour_structure):
        base_val = cell_neighbour_structure[1][1]
        try:
            sq_val = (cell_neighbour_structure[0][0] - base_val) ** 2 + \
                     (cell_neighbour_structure[0][1] - base_val) ** 2 + \
                     (cell_neighbour_structure[0][2] - base_val) ** 2 + \
                     (cell_neighbour_structure[1][0] - base_val) ** 2 + \
                     (cell_neighbour_structure[1][2] - base_val) ** 2 + \
                     (cell_neighbour_structure[2][0] - base_val) ** 2 + \
                     (cell_neighbour_structure[2][1] - base_val) ** 2 + \
                     (cell_neighbour_structure[2][2] - base_val) ** 2
        except TypeError:
            return None
        tri = sq_val ** 0.5
        return tri
