from sqlalchemy import Table, Column, Integer, Float, ForeignKey


def create_subsidence_cell_db_table(metadata):
    subsidence_cell_db_table = Table("subsidence_cells", metadata,
                                     Column("voxel_id", Integer,
                                            ForeignKey("voxels.id", ondelete="CASCADE"),
                                            primary_key=True),
                                     Column("subsidence_model_id", Integer,
                                            ForeignKey("subsidence_models.id", ondelete="CASCADE"),
                                            primary_key=True),
                                     Column("subsidence", Float),
                                     Column("subsidence_mse", Float, default=None),
                                     )
    return subsidence_cell_db_table
