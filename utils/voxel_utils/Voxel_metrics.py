from sqlalchemy import update

from utils.start_db import engine, Tables


def update_voxel_in_db_from_voxel(updated_voxel):
    """
    Обновляет значения метрик скана в БД
    :param updated_scan: Объект скана для которого обновляются метрики
    :return:
    """
    with engine.connect() as db_connection:
        stmt = update(Tables.voxels_db_table) \
            .where(Tables.voxels_db_table.c.id == updated_voxel.id) \
            .values(id=updated_voxel.id,
                    vxl_name=updated_voxel.vxl_name,
                    X=updated_voxel.X,
                    Y=updated_voxel.Y,
                    Z=updated_voxel.Z,
                    step=updated_voxel.step,
                    len=updated_voxel.len,
                    R=round(updated_voxel.R),
                    G=round(updated_voxel.G),
                    B=round(updated_voxel.B),
                    scan_id=updated_voxel.scan_id,
                    vxl_mdl_id=updated_voxel.vxl_mdl_id)
        db_connection.execute(stmt)
        db_connection.commit()
