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

    scan = ScanDB("PIT")
    scan.load_scan_from_file(file_name="src/Pit_clean.txt")
    # for step in [0.5, 1, 1.5, 2, 2.5, 5, 10, 15, 20, 25, 50]:
    #     vm = VoxelModelDB(scan, step)
    #     dem_model = DemModelDB(vm)
    #     SMFilterPercentile(dem_model, k_value=1.75).filter_model()
    #     plane_model = PlaneModelDB(vm)
    #     SMFilterPercentile(plane_model, k_value=1.75).filter_model()

    vm = VoxelModelDB(scan, 1)
    plane_model = PlaneModelDB(vm)
    plane_model.plot_mse()
    # plane_model.plot()

    # dem_model = DemModelDB(vm)



    # plane_model.plot()
    # plane_model.plot_mse()
    # plane_model.plot_mse_hist(plane_model)



    # print(scan)
    # step = 50
    # for _ in range(5):
    #     vm = VoxelModelDB(scan, 10)
    #     plane_model = PlaneModelDB(vm)
    #
    #
    #     scan = ScanFilterForTrees(scan, plane_model, k_value=2.5).filter_scan()
    #     plane_model.delete_model()
    #
    #     print(scan)
    # scan.save_scan_in_file(file_name="src/F_N2_14.txt")

    # # scan.save_scan_in_file(file_name="src/FS_Lagoninha")
    # vm = VoxelModelDB(scan, 5)
    # plane_model = PlaneModelDB(vm)
    # scan = ScanFilterByModelMSE(scan, plane_model, k_value=2.5).create_new_filtered_scan()
    # # scan.save_scan_in_file(file_name="src/FS_Lagoninha_2.txt")
    #
    # vm = VoxelModelDB(scan, 5)
    # plane_model = PlaneModelDB(vm)
    # # plane_model.plot()
    # # plane_model.plot_mse()
    # # plane_model.plot_mse_hist(plane_model)








if __name__ == "__main__":
    main()
