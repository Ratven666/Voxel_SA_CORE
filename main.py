from classes.BiModelDB import BiModelDB
from classes.DemModelDB import DemModelDB
from classes.PlaneModelDB import PlaneModelDB
from classes.VoxelModelDB import VoxelModelDB
from db_models.dem_models_table import DemTypeEnum
from utils.logs.console_log_config import console_logger
from utils.scan_utils.scan_filters.ScanFilterByCellMSE import ScanFilterByCellMSE
from utils.scan_utils.scan_filters.ScanFilterByModelMSE import ScanFilterByModelMSE
from utils.scan_utils.scan_filters.ScanFilterForTrees import ScanFilterForTrees
from utils.scan_utils.scan_plotters.ScanPlotterPlotly import ScanPlotterPointsPlotly, ScanPlotterMeshPlotly
from utils.scan_utils.scan_samplers.TotalPointCountScanSampler import TotalPointCountScanSampler
from utils.scan_utils.scan_serializers.ScanJsonSerializer import ScanJsonSerializer
from utils.segmented_mdl_utils.segmented_models_expoters.DxfExporter import DxfExporter
from utils.segmented_mdl_utils.segmented_models_expoters.PlyExporter import PlyExporter
from utils.segmented_mdl_utils.segmented_models_filters.SMFilterByMaxMSE import SMFilterByMaxMSE
from utils.segmented_mdl_utils.segmented_models_filters.SMFilterByMaxPercentile import SMFilterByMaxPercentile
from utils.segmented_mdl_utils.segmented_models_filters.SMFilterPercentile import SMFilterPercentile
from utils.segmented_mdl_utils.segmented_models_plotters.HistMSEPlotterPlotly import HistMSEPlotterPlotly
from utils.segmented_mdl_utils.segmented_models_plotters.SegmentModelPlotly import SegmentModelPlotly
from utils.segmented_mdl_utils.segmented_models_serializers.SegmentedModelJsonSerializer import \
    SegmentedModelJsonSerializer

from utils.start_db import create_db

from classes.ScanDB import ScanDB
from utils.voxel_utils.voxel_model_plotters.Voxel_model_plotter import VoxelModelPlotter
from utils.voxel_utils.voxel_model_separators.FastVMSeparator import FastVMSeparator
from utils.voxel_utils.voxel_model_separators.VMBruteForceSeparatorWithoutVoxelScansPoints import \
    VMBruteForceSeparatorWithoutVoxelScansPoints
from utils.voxel_utils.voxel_model_serializers.VoxelModelJsonSerializer import VoxelModelJsonSerializer


def main():
    create_db()

    scan = ScanDB("TEST")
    scan.load_scan_from_file(file_name="src/KuchaRGB.txt")


    vm = VoxelModelDB(scan, 0.1, dx=0, dy=0, dz=0, is_2d_vxl_mdl=True)

    # dem = DemModelDB(vm)
    # plane = PlaneModelDB(vm)
    #
    bi_plane = BiModelDB(vm, DemTypeEnum.PLANE, enable_mse=True)

    dxf = DxfExporter(bi_plane, grid_densification=1, filtrate=True).export()
    ply = PlyExporter(bi_plane, grid_densification=1, filtrate=True).export()


if __name__ == "__main__":
    main()
