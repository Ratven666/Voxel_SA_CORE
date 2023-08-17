from sqlalchemy import Table, Column, Integer, String, ForeignKey


def create_meshes_db_table(metadata):
    meshes_db_table = Table("meshes", metadata,
                            Column("id", Integer, primary_key=True),
                            Column("mesh_name", String, nullable=False, unique=True, index=True),
                            Column("len", Integer, default=0),
                            Column("base_scan_id", Integer, ForeignKey("scans.id"))
                            )
    return meshes_db_table
