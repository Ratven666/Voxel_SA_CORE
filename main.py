from time import time

from classes.VoxelModelDB import VoxelModelDB

from utils.plotters.ScanPlotterMPL import ScanPlotterMPL
from utils.plotters.ScanPlotterPlotly import ScanPlotterMeshPlotly, ScanPlotterPlotly
from utils.plotters.ScanPlotterPlotly import ScanPlotterPointsPlotly
from utils.scan_utils.scan_samplers.TotalPointCountScanSampler import TotalPointCountScanSampler
from utils.start_db import create_db, engine, Tables

from classes.ScanDB import ScanDB

def main():
    create_db()


    time0 = time()
    scan = ScanDB("Kucha")
    print(scan)
    print(time() - time0)

    time0 = time()
    scan.load_scan_from_file()
    print(scan)
    print(time() - time0)


    time0 = time()
    # vm = VoxelModelDB(scan, 0.05, is_2d_vxl_mdl=False)

    # scan.plot(plotter=ScanPlotterMPL(point_size=5))
    # scan.plot(plotter=ScanPlotterPointsPlotly(sampler=TotalPointCountScanSampler(10_000)))
    scan.plot(plotter=ScanPlotterMeshPlotly(sampler=TotalPointCountScanSampler(1_000)))
    print(time() - time0)


if __name__ == "__main__":
    main()
