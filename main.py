from classes.DemModelDB import DemModelDB
from classes.PlaneModelDB import PlaneModelDB
from classes.VoxelModelDB import VoxelModelDB
from utils.logs.console_log_config import console_logger
from utils.scan_utils.scan_plotters.ScanPlotterPlotly import ScanPlotterPointsPlotly, ScanPlotterMeshPlotly
from utils.scan_utils.scan_samplers.TotalPointCountScanSampler import TotalPointCountScanSampler

from utils.start_db import create_db

from classes.ScanDB import ScanDB
from utils.voxel_utils.voxel_model_plotters.Voxel_model_plotter import VoxelModelPlotter
from utils.voxel_utils.voxel_model_separators.VMBruteForceSeparatorWithoutVoxelScansPoints import \
    VMBruteForceSeparatorWithoutVoxelScansPoints


def main():
    create_db()

    scan = ScanDB("Tank")
    print(scan)

    scan.load_scan_from_file()
    print(scan)

    vm = VoxelModelDB(scan, 0.5, is_2d_vxl_mdl=True,
                      voxel_model_separator=VMBruteForceSeparatorWithoutVoxelScansPoints())
    print(vm)

    # scan.plot(plotter=ScanPlotterPointsPlotly(sampler=TotalPointCountScanSampler(50_000)))
    # scan.plot(plotter=ScanPlotterMeshPlotly(sampler=TotalPointCountScanSampler(10_000)))
    # scan.plot()
    # vm.plot(VoxelModelPlotter())
    dem_model = DemModelDB(vm, min_voxel_len=1000)
    plane_model = PlaneModelDB(vm, min_voxel_len=1)
    # print(dem_model)


    dem_model.plot_mse()

    dem_model.plot()
    # plane_model.plot()

if __name__ == "__main__":
    main()
