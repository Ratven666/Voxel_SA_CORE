from sqlalchemy import Table, Column, Integer, Float, ForeignKey


def create_polynomial_2_cell_db_table(metadata):
    polynomial_2_cell_db_table = Table("polynomial_2_cells", metadata,
                                       Column("voxel_id", Integer,
                                              ForeignKey("voxels.id", ondelete="CASCADE"),
                                              primary_key=True),
                                       Column("base_model_id", Integer,
                                              ForeignKey("dem_models.id", ondelete="CASCADE"),
                                              primary_key=True),
                                       Column("A", Float),
                                       Column("B", Float),
                                       Column("C", Float),
                                       Column("D", Float),
                                       Column("E", Float),
                                       Column("F", Float),
                                       Column("mA", Float),
                                       Column("mB", Float),
                                       Column("mC", Float),
                                       Column("mD", Float),
                                       Column("mE", Float),
                                       Column("mF", Float),
                                       Column("r", Integer),
                                       Column("MSE", Float, default=None)
                                       )
    return polynomial_2_cell_db_table
