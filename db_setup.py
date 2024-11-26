import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_protocol import Base
from models import Organization, Shop
from services.constants import ORGANIZATIONS, SHOPS


class DatabaseSetup:
    def __init__(self) -> None:
        """
        Initialize the db connection.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, "food_bank.db")
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def insert_data(self) -> None:
        with self.SessionLocal() as session:
            # insert orgs
            orgs = [Organization(name=name) for name in ORGANIZATIONS]
            session.add_all(orgs)

            # insert shops
            shops = [Shop(name=name) for name in SHOPS]
            session.add_all(shops)

            session.commit()


if __name__ == "__main__":
    db_setup = DatabaseSetup()
    db_setup.insert_data()
