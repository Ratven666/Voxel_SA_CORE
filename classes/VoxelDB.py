class VoxelDB:

    def __init__(self, X, Y, Z, step, vxl_mdl_id):
        self.id = None
        self.X = X
        self.Y = Y
        self.Z = Z
        self.step = step
        self.scan_id = None
        self.vxl_mdl_id = vxl_mdl_id
        self.vxl_name = self.__name_generator()

    def __name_generator(self):
        return (f"VXL_VM:{self.vxl_mdl_id}_s{self.step}_"
                f"X:{round(self.X, 5)}_"
                f"Y:{round(self.Y, 5)}_"
                f"Z:{round(self.Z, 5)}"
                )

    def __str__(self):
        return (f"{self.__class__.__name__} "
                f"[id: {self.id},\tName: {self.vxl_name}\t\t"
                f"X: {round(self.X, 5)}\tY: {round(self.Y, 5)}\tZ: {round(self.Z, 5)}]"
                )

    def __repr__(self):
        return f"{self.__class__.__name__} [ID: {self.id}]"
