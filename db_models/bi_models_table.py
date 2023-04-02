from sqlalchemy import Table, Column, Integer, String, ForeignKey, Text


def create_bi_models_db_table(metadata):
    bi_models_db_table = Table("bi_models", metadata,
                               Column("id", Integer, primary_key=True),
                               Column("base_voxel_model_id", Integer,
                                      ForeignKey("voxel_models.id")),
                               Column("base_segment_model_name", String, nullable=False, unique=True),
                               Column("bi_model_name", String, nullable=False, unique=True),
                               Column("MSE_data", Text, default=None)
                               )
    return bi_models_db_table
