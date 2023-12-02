from abc import ABC, abstractmethod


class SegmentedModelToScanABC(ABC):

    def __init__(self, segmented_model):
        self.segmented_model = segmented_model

    @abstractmethod
    def export_to_scan(self):
        pass
