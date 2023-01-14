from sqlalchemy import Table, Column, Integer, String, Float


def create_scans_db_table(metadata):
    scans_db_table = Table("scans", metadata,
                           Column("id", Integer, primary_key=True),
                           Column("name", String, nullable=False, unique=True),
                           Column("len", Integer),
                           Column("min_X", Float),
                           Column("max_X", Float),
                           Column("min_Y", Float),
                           Column("max_Y", Float),
                           Column("min_Z", Float),
                           Column("max_Z", Float),
                           )
    return scans_db_table
