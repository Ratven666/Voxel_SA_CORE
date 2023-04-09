from classes.BiModelDB import BiModelDB
from classes.DemModelDB import DemModelDB
from classes.PlaneModelDB import PlaneModelDB
from classes.VoxelModelDB import VoxelModelDB
from db_models.dem_models_table import DemTypeEnum
from utils.logs.console_log_config import console_logger
from utils.scan_utils.scan_plotters.ScanPlotterPlotly import ScanPlotterPointsPlotly, ScanPlotterMeshPlotly
from utils.scan_utils.scan_samplers.TotalPointCountScanSampler import TotalPointCountScanSampler
from utils.segmented_mdl_utils.segmented_models_plotters.SegmentModelPlotly import SegmentModelPlotly

from utils.start_db import create_db

from classes.ScanDB import ScanDB
from utils.voxel_utils.voxel_model_plotters.Voxel_model_plotter import VoxelModelPlotter
from utils.voxel_utils.voxel_model_separators.FastVMSeparator import FastVMSeparator
from utils.voxel_utils.voxel_model_separators.VMBruteForceSeparatorWithoutVoxelScansPoints import \
    VMBruteForceSeparatorWithoutVoxelScansPoints


def main():
    create_db()

    scan = ScanDB("Kucha")
    print(scan)

    scan.load_scan_from_file()

    # scan.plot()
    # scan.plot(plotter=ScanPlotterPointsPlotly(sampler=TotalPointCountScanSampler(100_000)))
    # scan.plot(plotter=ScanPlotterMeshPlotly(sampler=TotalPointCountScanSampler(20_000)))
    steps = [10, 5, 2.5, 1, 0.5, 0.25, 0.1]
    for step in steps:
        vm = VoxelModelDB(scan, step, is_2d_vxl_mdl=True,
                          voxel_model_separator=FastVMSeparator())
        print(vm)
        # vm.plot(VoxelModelPlotter())

        # dem_model = DemModelDB(vm)
        # plane_model = PlaneModelDB(vm)
        bi_dem_model_mse = BiModelDB(vm, DemTypeEnum.DEM, enable_mse=True)
        bi_dem_model = BiModelDB(vm, DemTypeEnum.DEM, enable_mse=False)
        bi_plane_model_mse = BiModelDB(vm, DemTypeEnum.PLANE, enable_mse=True)
        bi_plane_model = BiModelDB(vm, DemTypeEnum.PLANE, enable_mse=False)

        print("!" * 1000)


    # bi_plane_model_mse.delete_model()
    # bi_dem_model_mse.delete_model()
    # dem_model.delete_model()
    # plane_model.delete_model()
    #

    # dem_model.plot_mse()
    # bi_dem_model_mse.plot_mse()
    # bi_dem_model.plot_mse()
    # plane_model.plot_mse()
    # bi_plane_model_mse.plot_mse()
    # bi_plane_model.plot_mse()
    #


    # dem_model.plot(plotter=SegmentModelPlotly())
    # plane_model.plot()
    # bi_dem_model.plot()
    # bi_plane_model.plot()
#


if __name__ == "__main__":
    main()
