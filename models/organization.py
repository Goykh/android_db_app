from sqlalchemy import Integer, Column, String

from . import Base


class Organization(Base):
    __tablename__ = "organization"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
