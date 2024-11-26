from sqlalchemy import Column, Integer, String

from . import Base


class Organization(Base):
    __tablename__ = "organization"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
