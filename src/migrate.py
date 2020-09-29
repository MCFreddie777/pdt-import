from sqlalchemy import create_engine, MetaData
from sqlalchemy.schema import DropTable
from config.connection import db_string
from database.models import models

def drop_tables(engine,exclude_tables):
    meta = MetaData(engine)
    meta.reflect(bind=engine)
    connection = engine.connect()

    for tbl in meta.sorted_tables:
        if tbl.name not in exclude_tables:
            connection.execute(DropTable(tbl))

def migrate(engine,models):
    for model in models:
        model.create(engine)


engine = create_engine(db_string)
RESERVED_TABLES = ['spatial_ref_sys']

drop_tables(engine,RESERVED_TABLES)
migrate(engine,models)
