from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey


def create_voxels_db_table(metadata):
    voxels_db_table = Table("voxels", metadata,
                            Column("id", Integer, primary_key=True),
                            Column("vxl_name", String, nullable=False, unique=True, index=True),
                            Column("x0", Float),
                            Column("y0", Float),
                            Column("z0", Float),
                            Column("step", Float, nullable=False),
                            Column("scan_id", Integer, ForeignKey("scans.id", ondelete="CASCADE")),
                            Column("vxl_mdl_id", Integer, ForeignKey("voxel_models.id"))
                            )
    return voxels_db_table
