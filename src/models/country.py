from sqlalchemy import Column, String, Integer, Index
from sqlalchemy.orm import relationship
from base import Base


class Country(Base):
    __tablename__ = 'countries'

    # properties
    id = Column('id', Integer, primary_key=True)
    code = Column('code', String(2))
    name = Column('name', String(200))
    __table_args__ = (Index('country_composite', "code", "name"),)

    # relationships
    tweets = relationship("Tweet")

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        return f"code: {self.code}\nname: {self.name}\n"
