from classes.DemModelDB import DemModelDB
from classes.VoxelModelDB import VoxelModelDB
from utils.logs.console_log_config import console_logger
from utils.scan_utils.scan_plotters.ScanPlotterPlotly import ScanPlotterPointsPlotly, ScanPlotterMeshPlotly
from utils.scan_utils.scan_samplers.TotalPointCountScanSampler import TotalPointCountScanSampler

from utils.start_db import create_db

from classes.ScanDB import ScanDB
from utils.voxel_utils.voxel_model_plotters.Voxel_model_plotter import VoxelModelPlotter


def main():
    create_db()

    scan = ScanDB("Tank")
    print(scan)

    scan.load_scan_from_file()
    print(scan)

    vm = VoxelModelDB(scan, 1, is_2d_vxl_mdl=False)
    print(vm)

    # scan.plot(plotter=ScanPlotterPointsPlotly(sampler=TotalPointCountScanSampler(50_000)))
    # scan.plot(plotter=ScanPlotterMeshPlotly(sampler=TotalPointCountScanSampler(10_000)))
    # scan.plot()
    # vm.plot(VoxelModelPlotter())
    dem_model = DemModelDB(vm)
    print(dem_model)

    for el in dem_model:
        print(el, el.avr_z, el.voxel.len)

    dem_model.plot()

if __name__ == "__main__":
    main()
