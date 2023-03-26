from time import time

from classes.VoxelModelDB import VoxelModelDB
from utils.plotters.ScanPlotterPlotly import ScanPlotterPointsPlotly, ScanPlotterMeshPlotly
from utils.scan_utils.scan_samplers.TotalPointCountScanSampler import TotalPointCountScanSampler

from utils.start_db import create_db

from classes.ScanDB import ScanDB


def main():
    create_db()


    time0 = time()
    scan = ScanDB("KuchaRGB")
    print(scan)
    print(time() - time0)

    time0 = time()
    scan.load_scan_from_file()
    print(scan)
    print(time() - time0)


    time0 = time()
    vm = VoxelModelDB(scan, 0.5, is_2d_vxl_mdl=False)
    print(vm)
    # for idx, v in enumerate(vm):
    #     print(idx, v)

    scan.plot(plotter=ScanPlotterPointsPlotly(sampler=TotalPointCountScanSampler(50_000)))
    # scan.plot(plotter=ScanPlotterMeshPlotly(sampler=TotalPointCountScanSampler(10_000)))
    print(time() - time0)

    # vm.plot(VoxelModelPlotter())
    vm.plot()

if __name__ == "__main__":
    main()
