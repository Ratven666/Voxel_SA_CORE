from abc import abstractmethod

from classes.branch_classes.terrain_indexes.DEMIndexABC import DEMIndexABC


class TerrainRuggednessIndexABC(DEMIndexABC):
    def __init__(self, dem_model, full_neighbours=False):
        self.value = 0
        self.n = 0
        super().__init__(dem_model, full_neighbours)

    def _do_prepare_actions(self, cell_neighbour_structure):
        self.base_val = cell_neighbour_structure[1][1]
        self.neighbours = [cell_neighbour_structure[0][0],
                           cell_neighbour_structure[0][1],
                           cell_neighbour_structure[0][2],
                           cell_neighbour_structure[1][0],
                           cell_neighbour_structure[1][2],
                           cell_neighbour_structure[2][0],
                           cell_neighbour_structure[2][1],
                           cell_neighbour_structure[2][2],
                           ]

    @abstractmethod
    def _do_prepare_calculation(self, neighbour):
        pass

    @abstractmethod
    def _calc_tri(self):
        pass

    def calk_index_value(self, cell_neighbour_structure):
        self._do_prepare_actions(cell_neighbour_structure)
        for neighbour in self.neighbours:
            try:
                self._do_prepare_calculation(neighbour)
            except TypeError:
                if self.full_neighbours is True:
                    return None
                continue
        tri = self._calc_tri() if self.n != 0 else None
        self.value = 0
        self.n = 0
        return tri


class TerrainRuggednessIndexClassic(TerrainRuggednessIndexABC):
    def __init__(self, dem_model, full_neighbours=True):
        super().__init__(dem_model, full_neighbours=True)
        self.index_name = "TRI_Classic"

    def _do_prepare_calculation(self, neighbour):

        self.value += (neighbour - self.base_val) ** 2
        self.n += 1

    def _calc_tri(self):
        return self.value ** 0.5


class TerrainRuggednessIndexClassicModify(TerrainRuggednessIndexClassic):
    def __init__(self, dem_model, full_neighbours=False):
        super().__init__(dem_model, full_neighbours)
        self.full_neighbours = full_neighbours
        self.index_name = "TRI_Classic_Modify"


class TerrainRuggednessIndexABSValue(TerrainRuggednessIndexABC):
    def __init__(self, dem_model, full_neighbours=False):
        super().__init__(dem_model, full_neighbours)
        self.index_name = "TRI_ABS_Value"


    def _do_prepare_calculation(self, neighbour):
        self.value += abs(neighbour - self.base_val)
        self.n += 1

    def _calc_tri(self):
        return self.value / self.n


class MyTerrainRuggednessIndex(TerrainRuggednessIndexABC):
    def __init__(self, dem_model, full_neighbours=False):
        super().__init__(dem_model, full_neighbours)
        self.index_name = "My_TRI"


    def _do_prepare_calculation(self, neighbour):
        self.value += (neighbour - self.base_val)
        self.n += 1

    def _calc_tri(self):
        return abs(self.value) / self.n
