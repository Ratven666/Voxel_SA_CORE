from classes.abc_classes.VoxelModelABC import VoxelModelABC


class VoxelModelLite(VoxelModelABC):

    def __init__(self, scan, step, dx, dy, dz, is_2d_vxl_mdl=True):
        super().__init__(scan, step, dx, dy, dz, is_2d_vxl_mdl)
        self.voxel_structure = []

    def __iter__(self):
        return iter(self.voxel_structure)