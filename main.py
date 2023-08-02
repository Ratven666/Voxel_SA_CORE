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
from utils.segmented_mdl_utils.segmented_models_filters.SMFilterByMaxMSE import SMFilterByMaxMSE
from utils.segmented_mdl_utils.segmented_models_filters.SMFilterByMaxPercentile import SMFilterByMaxPercentile
from utils.segmented_mdl_utils.segmented_models_filters.SMFilterPercentile import SMFilterPercentile
from utils.segmented_mdl_utils.segmented_models_plotters.HistMSEPlotterPlotly import HistMSEPlotterPlotly
from utils.segmented_mdl_utils.segmented_models_plotters.SegmentModelPlotly import SegmentModelPlotly

from utils.start_db import create_db

from classes.ScanDB import ScanDB
from utils.voxel_utils.voxel_model_plotters.Voxel_model_plotter import VoxelModelPlotter
from utils.voxel_utils.voxel_model_separators.FastVMSeparator import FastVMSeparator
from utils.voxel_utils.voxel_model_separators.VMBruteForceSeparatorWithoutVoxelScansPoints import \
    VMBruteForceSeparatorWithoutVoxelScansPoints


def main():
    create_db()

    scan = ScanDB("TEST")
    scan.load_scan_from_file(file_name="src/forest_full_1 m.txt")
    # scan.plot(plotter=ScanPlotterPointsPlotly())
    # scan.plot(plotter=ScanPlotterMeshPlotly(sampler=TotalPointCountScanSampler(1000)))
    vm = VoxelModelDB(scan, 5, dx=0, dy=0, dz=0, is_2d_vxl_mdl=True)
    vm = VoxelModelDB(scan, 5, dx=0.2, dy=0.2, dz=0.2, is_2d_vxl_mdl=True)
    vm = VoxelModelDB(scan, 5, dx=0.4, dy=0.4, dz=0.4, is_2d_vxl_mdl=True)
    vm = VoxelModelDB(scan, 5, dx=0.6, dy=0.6, dz=0.6, is_2d_vxl_mdl=True)
    vm = VoxelModelDB(scan, 5, dx=0.8, dy=0.8, dz=0.8, is_2d_vxl_mdl=True)
    vm = VoxelModelDB(scan, 5, dx=1, dy=1, dz=1, is_2d_vxl_mdl=True)
    vm = VoxelModelDB(scan, 5, dx=1.2, dy=1.2, dz=1.2, is_2d_vxl_mdl=True)
    vm = VoxelModelDB(scan, 5, dx=0, dy=0, dz=0, is_2d_vxl_mdl=False)
    vm = VoxelModelDB(scan, 5, dx=0.2, dy=0.2, dz=0.2, is_2d_vxl_mdl=False)
    vm = VoxelModelDB(scan, 5, dx=0.4, dy=0.4, dz=0.4, is_2d_vxl_mdl=False)
    vm = VoxelModelDB(scan, 5, dx=0.6, dy=0.6, dz=0.6, is_2d_vxl_mdl=False)
    vm = VoxelModelDB(scan, 5, dx=0.8, dy=0.8, dz=0.8, is_2d_vxl_mdl=False)
    vm = VoxelModelDB(scan, 5, dx=1, dy=1, dz=1, is_2d_vxl_mdl=False)
    vm = VoxelModelDB(scan, 5, dx=1.2, dy=1.2, dz=1.2, is_2d_vxl_mdl=False)
    # vm.plot()
    # sm_dem = DemModelDB(vm)
    # sm_dem = BiModelDB(vm, DemTypeEnum.DEM)
    #
    # sm_plane = PlaneModelDB(vm)
    # sm_plane = BiModelDB(vm, DemTypeEnum.PLANE)
    # sm_dem.plot()
    # sm_plane.plot()


if __name__ == "__main__":
    main()
