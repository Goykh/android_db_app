from sqlalchemy import Integer, Column, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from . import Base


class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id"))
    shop_id = Column(Integer, ForeignKey("shop.id"))
    type = Column(String)
    amount = Column(Float)
    organization = relationship("Organization", backref="transactions")
    shop = relationship("Shop", backref="transactions")