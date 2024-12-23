from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Donation(Base):
    # TODO: rename table and model to donation
    __tablename__ = "donations"
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    shop_id = Column(Integer, ForeignKey("shop.id"), nullable=False)
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)

    organization = relationship("Organization", backref="donations")
    shop = relationship("Shop", backref="donations")
