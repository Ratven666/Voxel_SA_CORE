from sqlalchemy import Table, Column, Integer, String, ForeignKey, Text


def create_plane_models_db_table(metadata):
    plane_models_db_table = Table("plane_models", metadata,
                                  Column("base_voxel_model_id", Integer, ForeignKey("voxel_models.id")),
                                  Column("plane_model_name", String, nullable=False, unique=True, index=True),
                                  Column("MSE_data", Text, default=None)
                                  )
    return plane_models_db_table
