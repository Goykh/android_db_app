from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Donation(Base):
    __tablename__ = "donations"
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    shop_id = Column(Integer, ForeignKey("shop.id"), nullable=False)
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    create_date = Column(DateTime, default=datetime.now, nullable=False)

    organization = relationship("Organization", backref="donations")
    shop = relationship("Shop", backref="donations")
