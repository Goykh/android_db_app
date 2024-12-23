import os

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from xlsxwriter import Workbook

from models import Base, Donation, Organization, Shop
from services.date import get_current_date


class DatabaseProtocol:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, "food_bank.db")

        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def check_record_exists(self, name: str, model: type[Base], column_name: str = "name") -> bool:
        """
        Check if an org already exists
        :param name: org name
        :param model: db model
        :param column_name: name of column to search in
        :return: True if exists, else False
        """
        with self.SessionLocal() as session:
            column = getattr(model, column_name)
            stmt = select(1).where(column == name).limit(1)
            result = session.execute(stmt).scalar()
            return result is not None

    def create_record(self, model: type[Base], name: str) -> None:
        """
        Creates a new database record.
        :param model: model name
        :param name: record name
        :return: None
        """
        with self.SessionLocal() as session:
            new_record = model(name=name)
            session.add(new_record)
            session.commit()
            session.refresh(new_record)

    def get_all_records(self, model: type[Base]) -> list[type[Base]]:
        """
        Gets all records from a table.
        :param model: table model
        :return: a list of all records
        """
        with self.SessionLocal() as session:
            records = session.query(model).all()
            return records

    def get_organization_donations(self, organization_id: int) -> list[tuple[str, str, float]]:
        """
        Gets the donations of the given organization ID.
        :param organization_id: id of organization
        :return: a list of tuples with the shop name, type and amount
        """
        with self.SessionLocal() as session:
            # TODO: Test this
            donations = (
                session.query(
                    Shop.name.label("shop_name"), Donation.type, func.sum(Donation.amount).label("total_amount")
                )
                .join(Shop, Shop.id == Donation.shop_id)
                .filter(Donation.organization_id == organization_id)
                .group_by(Donation.shop_id, Donation.type)
                .all()
            )
            return donations

    def to_xlsx_file(self):
        # TODO: Add some logging so we know where to look if something goes wrong
        orgs = self.get_all_records(Organization)
        date = get_current_date()
        workbook = Workbook(f"/storage/emulated/0/documents/{date}.xslx")
        # TODO: add the android specific stuff
        for org in orgs:
            donations = self.get_organization_donations(org.id)
            if not donations:
                # there is nothing so skip
                continue
            worksheet = workbook.add_worksheet(org.name)
            for i, donation in enumerate(donations):
                worksheet.write(i, 0, donation[0])
                worksheet.write(i, 1, donation[1])
                worksheet.write(i, 2, donation[2])
