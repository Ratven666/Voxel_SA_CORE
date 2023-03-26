from classes.ScanLite import ScanLite
from classes.abc_classes.VoxelABC import VoxelABC


class VoxelLite(VoxelABC):
    """
    Воксель не связанный с базой данных
    """
    __slots__ = ["id", "X", "Y", "Z", "step", "vxl_mdl_id", "vxl_name", "scan_id", "len", "R", "G", "B"]

    def __init__(self, X, Y, Z, step, vxl_mdl_id):
        super().__init__(X, Y, Z, step, vxl_mdl_id)
        self.scan = ScanLite(f"SC_{self.vxl_name}")
