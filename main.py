from time import time

from classes.VoxelModelDB import VoxelModelDB
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


    # time0 = time()
    # for point in scan:
    #     pass
    # print(time() - time0)

    time0 = time()
    vm = VoxelModelDB(scan, 0.05, is_2d_vxl_mdl=False)
    # print(vm)
    # print(time() - time0)
    #
    # iter(vm)
    # time0 = time()
    scan.plot()
    print(time() - time0)

    coont = 0
    for v in vm:
        # print(v)
        coont += 1

    print(coont)


if __name__ == "__main__":
    main()
