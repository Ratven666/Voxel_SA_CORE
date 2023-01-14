from sqlalchemy import and_, select, update
from sqlalchemy import func

# from classes.ScanDB import ScanDB
from utils.start_db import engine, Tables


def calc_scan_metrics(scan):
    with engine.connect() as db_connection:
        stmt = select(func.count(Tables.points_db_table.c.id).label("len"),
                      func.min(Tables.points_db_table.c.X).label("min_X"),
                      func.max(Tables.points_db_table.c.X).label("max_X"),
                      func.min(Tables.points_db_table.c.Y).label("min_Y"),
                      func.max(Tables.points_db_table.c.Y).label("max_Y"),
                      func.min(Tables.points_db_table.c.Z).label("min_Z"),
                      func.max(Tables.points_db_table.c.Z).label("max_Z")).where(and_(
            Tables.points_scans_db_table.c.point_id == Tables.points_db_table.c.id,
            Tables.points_scans_db_table.c.scan_id == Tables.scans_db_table.c.id,
            Tables.scans_db_table.c.id == scan.id
        ))
        scan_metrics = db_connection.execute(stmt).mappings().first()
        scan.len = scan_metrics["len"]
        scan.min_X, scan.max_X = scan_metrics["min_X"], scan_metrics["max_X"]
        scan.min_Y, scan.max_Y = scan_metrics["min_Y"], scan_metrics["max_Y"]
        scan.min_Z, scan.max_Z = scan_metrics["min_Z"], scan_metrics["max_Z"]
        return scan


def update_scan_in_db(updated_scan):
    with engine.connect() as db_connection:
        stmt = update(Tables.scans_db_table)\
            .where(Tables.scans_db_table.c.id == updated_scan.id)\
            .values(len=updated_scan.len,
                    min_X=updated_scan.min_X,
                    max_X=updated_scan.max_X,
                    min_Y=updated_scan.min_Y,
                    max_Y=updated_scan.max_Y,
                    min_Z=updated_scan.min_Z,
                    max_Z=updated_scan.max_Z)
        db_connection.execute(stmt)
        db_connection.commit()

# def check_scan_borders(scan: Scan, point_data: dict):
#     if scan.min_X is None:
#         scan.min_X, scan.max_X = point_data["X"], point_data["X"]
#         scan.min_Y, scan.max_Y = point_data["Y"], point_data["Y"]
#         scan.min_Z, scan.max_Z = point_data["Z"], point_data["Z"]
#     if point_data["X"] < scan.min_X:
#         scan.min_X = point_data["X"]
#     if point_data["X"] > scan.max_X:
#         scan.max_X = point_data["X"]
#     if point_data["Y"] < scan.min_Y:
#         scan.min_Y = point_data["Y"]
#     if point_data["Y"] > scan.max_Y:
#         scan.max_Y = point_data["Y"]
#     if point_data["Z"] < scan.min_Z:
#         scan.min_Z = point_data["Z"]
#     if point_data["Z"] > scan.max_Z:
#         scan.max_Z = point_data["Z"]
