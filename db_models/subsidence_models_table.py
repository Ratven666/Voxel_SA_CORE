from sqlalchemy import Table, Column, Integer, String, ForeignKey, Float


def create_subsidence_models_db_table(metadata):
    subsidence_models_db_table = Table("subsidence_models", metadata,
                                       Column("id", Integer, primary_key=True),
                                       Column("base_voxel_model_id", Integer,
                                              ForeignKey("voxel_models.id")),
                                       Column("reference_model_id", Integer,
                                              ForeignKey("dem_models.id")),
                                       Column("comparable_model_id", Integer,
                                              ForeignKey("dem_models.id")),
                                       Column("model_name", String, nullable=False, unique=True),
                                       Column("subsidence_offset", Float, default=0.0),
                                       )
    return subsidence_models_db_table
