from sqlalchemy import Table, Column, Integer, Float, ForeignKey


def create_subsidence_cell_db_table(metadata):
    subsidence_cell_db_table = Table("subsidence_cells", metadata,
                                     Column("voxel_id", Integer,
                                            ForeignKey("voxels.id", ondelete="CASCADE"),
                                            primary_key=True),
                                     Column("subsidence_model_id", Integer,
                                            ForeignKey("subsidence_models.id", ondelete="CASCADE"),
                                            primary_key=True),
                                     Column("reference_z", Float),
                                     Column("comparable_z", Float),
                                     Column("subsidence", Float),
                                     Column("subsidence_mse", Float, default=None),
                                     Column("subsidence_class", Float, default=None),
                                     Column("slope", Float, default=None),
                                     Column("curvature", Float, default=None),
                                     )
    return subsidence_cell_db_table
