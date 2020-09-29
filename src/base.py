from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.connection import db_string

engine = create_engine(db_string)
Session = sessionmaker(bind=engine)

Base = declarative_base()
