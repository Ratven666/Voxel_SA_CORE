from classes.branch_classes.terrain_indexes.DEMIndexABC import DEMIndexABC


class MyTerrainRuggednessIndex(DEMIndexABC):

    def __init__(self, dem_model, full_neighbours=False):
        super().__init__(dem_model, full_neighbours)

    def calk_index_value(self, cell_neighbour_structure):
        base_val = cell_neighbour_structure[1][1]
        neighbours = [cell_neighbour_structure[0][0],
                      cell_neighbour_structure[0][1],
                      cell_neighbour_structure[0][2],
                      cell_neighbour_structure[1][0],
                      cell_neighbour_structure[1][2],
                      cell_neighbour_structure[2][0],
                      cell_neighbour_structure[2][1],
                      cell_neighbour_structure[2][2],
                      ]
        sq_sum = 0
        n = 0
        for neighbour in neighbours:
            try:
                sq_sum += (neighbour - base_val)
                n += 1
            except TypeError:
                if self.full_neighbours is True:
                    return None
                continue
        tri = abs(sq_sum) / n if n != 0 else None
        return tri
