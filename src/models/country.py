from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from base import Base


class Country(Base):
    __tablename__ = 'countries'

    # properties
    id = Column('id', Integer, primary_key=True)
    code = Column('code', String(2))
    name = Column('name', String(200))

    # relationships
    tweets = relationship("Tweet")

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        return f"code: {self.code}\nname: {self.name}\n"
