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

    scan = ScanDB("E")
    print(scan)

    scan.load_scan_from_file()
    print(scan)

    vm_50 = VoxelModelDB(scan, 50)

    #
    # dem_model_50 = DemModelDB(vm_50)
    plane_model_50 = PlaneModelDB(vm_50)
    # scan = ScanFilterByModelMSE(scan, plane_model_50, k_value=2).filter_scan()
    # plane_model_50.delete_model()

    bi_plane_with_mse_50 = BiModelDB(vm_50, DemTypeEnum.PLANE, enable_mse=True)
    bi_plane_50 = BiModelDB(vm_50, DemTypeEnum.PLANE, enable_mse=False)

    # plane_model_250 = SMFilterPercentile(plane_model_50, k_value=1.5).filter_model()
    # dem_model_100 = SMFilterPercentile(dem_model_100).filter_model()
    # dem_model_50 = SMFilterPercentile(dem_model_50).filter_model()
    plane_model_50.plot()
    bi_plane_with_mse_50.plot()


    plane_model_50.plot_mse_hist(plane_model_50,
                                plotter=HistMSEPlotterPlotly(bin_size=1, plot_like_probability=True))
    # dem_model_100.plot_mse_hist(dem_model_250, dem_model_100,
    #                             plotter=HistMSEPlotterPlotly(bin_size=1))

    # dem_model_10.plot()


if __name__ == "__main__":
    main()
