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


def write_mse_cells(file_name, model):
    with open(f"{file_name}.txt", "w", encoding="utf-8") as file:
        data = []
        for cell in model:
            if cell.mse is not None:
                data.append(cell.mse)
        data.sort()
        for mse in data:
            file.write(f"{mse}\n")

def main():
    create_db()

    scan = ScanDB("PIT")
    # scan.load_scan_from_file(file_name="src/balakovo2021_col.txt")
    # for step in [1, 1.5, 2, 2.5, 5, 10, 15, 20, 25, 50]:
    #     vm = VoxelModelDB(scan, step)
    #     dem_model = DemModelDB(vm)
    #     # dem_file = f"{scan.scan_name}_DEM_{step}"
    #     # write_mse_cells(dem_file, dem_model)
    #     SMFilterPercentile(dem_model).filter_model()
    #     # SMFilterPercentile(dem_model, k_value=1.5).filter_model()
    #     plane_model = PlaneModelDB(vm)
    #     SMFilterPercentile(plane_model).filter_model()
    #
    #     # plane_file = f"{scan.scan_name}_PLANE_{step}"
    #     # write_mse_cells(plane_file, plane_model)


        # SMFilterByMaxPercentile(plane_model, max_percentile=0.98).filter_model()
        # SMFilterPercentile(plane_model, k_value=1.5).filter_model()

    #
    # #
    vm = VoxelModelDB(scan, 2)
    plane_model = PlaneModelDB(vm)
    # dem_model = DemModelDB(vm)
    # plane_model.plot()
    plane_model.plot_mse()
    # dem_model.plot_mse()
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
