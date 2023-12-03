import random

from classes.ScanLite import ScanLite
from classes.abc_classes.ScanABC import ScanABC


def separate_scan(base_scan:ScanABC, count_of_scans, random_seed=None, save_in_db=True):
    if random_seed is not None:
        random.seed(random_seed)
    scans = [ScanLite(scan_name=f"{base_scan.scan_name}_({count + 1}_from_{count_of_scans})_rs_{random_seed}")
             for count in range(count_of_scans)]
    if random_seed is not None:
        random.seed(random_seed)
    for point in base_scan:
        index = random.randint(0, count_of_scans - 1)
        scans[index].add_point(point)
    if save_in_db:
        for idx, scan in enumerate(scans):
            scans[idx] = scan.save_to_db()
    return scans
