from classes.BiModelDB import BiModelDB
from classes.DemModelDB import DemModelDB
from classes.PlaneModelDB import PlaneModelDB
from classes.VoxelModelDB import VoxelModelDB
from db_models.dem_models_table import DemTypeEnum
from utils.logs.console_log_config import console_logger
from utils.scan_utils.scan_filters.ScanFilterByCellMSE import ScanFilterByCellMSE
from utils.scan_utils.scan_filters.ScanFilterByModelMSE import ScanFilterByModelMSE
from utils.scan_utils.scan_plotters.ScanPlotterPlotly import ScanPlotterPointsPlotly, ScanPlotterMeshPlotly
from utils.scan_utils.scan_samplers.TotalPointCountScanSampler import TotalPointCountScanSampler
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

    scan = ScanDB("E")
    print(scan)

    scan.load_scan_from_file()
    print(scan)

    vm_250 = VoxelModelDB(scan, 250)
    vm_100 = VoxelModelDB(scan, 100)
    vm_50 = VoxelModelDB(scan, 50)
    vm_25 = VoxelModelDB(scan, 25)
    vm_10 = VoxelModelDB(scan, 10)

    dem_model_250 = DemModelDB(vm_250)
    dem_model_100 = DemModelDB(vm_100)
    dem_model_50 = DemModelDB(vm_50)
    dem_model_25 = DemModelDB(vm_25)
    dem_model_10 = DemModelDB(vm_10)
    # scan = ScanFilterByModelMSE(scan, dem_model_50, k_value=2.5).filter_scan()
    # dem_model_50.delete_model()


    dem_model_100.plot_mse_hist(dem_model_250, dem_model_100, dem_model_50, dem_model_25, dem_model_10,
                                plotter=HistMSEPlotterPlotly(bin_size=1, plot_like_probability=True))
    # dem_model_100.plot_mse_hist(dem_model_250, dem_model_100,
    #                             plotter=HistMSEPlotterPlotly(bin_size=1))

    # dem_model_10.plot()


if __name__ == "__main__":
    main()
