from sqlalchemy import MetaData
from sqlalchemy.schema import DropTable
from base import engine, Base
from models.country import Country
from models.account import Account
from models.hashtag import Hashtag
from models.tweet import Tweet

def drop_tables(engine,exclude_tables):
    meta = MetaData(engine)
    meta.reflect(bind=engine)
    connection = engine.connect()

    for tbl in reversed(meta.sorted_tables):
        if tbl.name not in exclude_tables:
            connection.execute(DropTable(tbl))


RESERVED_TABLES = ['spatial_ref_sys']
drop_tables(engine,RESERVED_TABLES)

Base.metadata.create_all(engine)
