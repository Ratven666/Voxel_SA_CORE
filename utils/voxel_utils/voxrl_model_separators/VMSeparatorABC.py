from abc import ABC, abstractmethod


class VMSeparatorABC(ABC):

    @abstractmethod
    def separate_voxel_model(self, voxel_model, scan):
        pass
