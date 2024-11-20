from sqlalchemy import Integer, Column, String

from . import Base


class Shop(Base):
    __tablename__ = "shop"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
