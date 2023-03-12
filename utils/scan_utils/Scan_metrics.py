from sqlalchemy import and_, select, update
from sqlalchemy import func

from utils.start_db import engine, Tables


def calk_scan_metrics(scan_id):
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
            Tables.scans_db_table.c.id == scan_id
        ))
        scan_metrics = dict(db_connection.execute(stmt).mappings().first())
        scan_metrics["id"] = scan_id
        return scan_metrics


def update_scan_metrics(scan):
    """
    Рассчитывает значения метрик скана по точкам загруженным в БД
    средствами SQL и обновляет их в самом скане
    :param scan: скан для которого рассчитываются и в котором обновляются метрики
    :return: скан с обновленными  метриками
    """
    scan_metrics = calk_scan_metrics(scan_id=scan.id)
    scan.len = scan_metrics["len"]
    scan.min_X, scan.max_X = scan_metrics["min_X"], scan_metrics["max_X"]
    scan.min_Y, scan.max_Y = scan_metrics["min_Y"], scan_metrics["max_Y"]
    scan.min_Z, scan.max_Z = scan_metrics["min_Z"], scan_metrics["max_Z"]
    return scan


def update_scan_in_db_from_scan_metrics(scan_metrics: dict):
    """
        Обновляет значения метрик скана в БД
        :param scan_metrics: Объект скана для которого обновляются метрики   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        :return:
        """
    with engine.connect() as db_connection:
        stmt = update(Tables.scans_db_table) \
            .where(Tables.scans_db_table.c.id == scan_metrics["id"]) \
            .values(len=scan_metrics["len"],
                    min_X=scan_metrics["min_X"],
                    max_X=scan_metrics["max_X"],
                    min_Y=scan_metrics["min_Y"],
                    max_Y=scan_metrics["max_Y"],
                    min_Z=scan_metrics["min_Z"],
                    max_Z=scan_metrics["max_Z"])
        db_connection.execute(stmt)
        db_connection.commit()


def update_scan_in_db_from_scan(updated_scan):
    """
    Обновляет значения метрик скана в БД
    :param updated_scan: Объект скана для которого обновляются метрики
    :return:
    """
    with engine.connect() as db_connection:
        stmt = update(Tables.scans_db_table) \
            .where(Tables.scans_db_table.c.id == updated_scan.id) \
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
