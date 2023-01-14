from time import time


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

    print(engine.dialect.name)

    time0 = time()
    for point in scan:
        pass
    print(time() - time0)

    time0 = time()
    scan.plot()
    print(time() - time0)


if __name__ == "__main__":
    main()
