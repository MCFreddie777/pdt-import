from sqlalchemy import create_engine, MetaData
from sqlalchemy.schema import DropTable
from config.connection import db_string
from database.tables import meta

def drop_tables(engine,exclude_tables):
    meta = MetaData(engine)
    meta.reflect(bind=engine)
    connection = engine.connect()

    for tbl in reversed(meta.sorted_tables):
        if tbl.name not in exclude_tables:
            connection.execute(DropTable(tbl))


engine = create_engine(db_string)
RESERVED_TABLES = ['spatial_ref_sys']
drop_tables(engine,RESERVED_TABLES)
meta.create_all(engine)
