import os

from kivy.logger import Logger
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from xlsxwriter import Workbook

from models import Base, Donation, Organization, Shop
from services.date import get_current_date


class DatabaseProtocol:
    def __init__(self) -> None:
        Logger.info("PB_APP: Connecting to database...")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, "food_bank.db")

        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        Logger.info("PB_APP: Connected to database.")

        Logger.info("PB_APP: Creating database session...")
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
        Logger.info("PB_APP: Created database session.")

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

    def get_record_by_name(self, model: type[Base], name: str) -> list[type[Base]] | None:
        """
        Returns a record of the given model.
        Should always return only one record as the name column is unique.
        :param model: given model (Shop or Organization)
        :param name: name of the record
        :return: if found record, else nothing
        """
        with self.SessionLocal() as session:
            record = session.query(model).filter(model.name == name).all()
            return record or None

    def delete_record(self, model: type[Base], record_id: int) -> bool | None:
        """
        Deletes a record of the given model by its id.
        Verifies if the record exists first.
        :param model: given model (Shop or Organization)
        :param record_id: ID of record to be deleted
        :return: True on success, else None
        """
        with self.SessionLocal() as session:
            record = session.query(model).get(record_id)
            if not record:
                return
            try:
                # in case of constraints on donation table...
                session.delete(record)
                session.commit()
                Logger.info(f"PB_APP: Deleted record id={record.id}; name={record.name}.")
                return True
            except Exception:
                # TODO: Log exception also to some file!!!
                Logger.exception(f"PB_APP: Failed deletion of record: id={record.id}; name={record.name}.")
                session.rollback()
                return

    def make_donation(self, org: Organization, shop: Shop, donation_type: str, amount: float) -> True | None:
        """
        Creates a donation record.
        :param org: selected org
        :param shop: selected shop
        :param donation_type: type of donation
        :param amount: amount as float
        :return: True on success, else None
        """
        with self.SessionLocal() as session:
            try:
                donation = Donation(
                    organization_id=org.id,
                    shop_id=shop.id,
                    type=donation_type,
                    amount=amount,
                )
                session.add(donation)
                session.commit()
                Logger.info("PB_APP: Created new donation.")
                return True
            except Exception:
                Logger.exception("PB_APP: Could not create new donation.")

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

    def get_detailed_organization_donations(self, organization_id: int) -> list[type[Donation]]:
        """
        Returns all donation records matching the given organization.
        :param organization_id: given org id
        :return: list of Donation records
        """
        with self.SessionLocal() as session:
            return session.query(Donation).filter(Donation.organization_id == organization_id).all()

    def to_xlsx_file(self) -> None:
        # TODO Test versions of this method on android
        #  from android.permissions import request_permissions, Permission
        #  request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        orgs = self.get_all_records(Organization)
        date = get_current_date()
        Logger.info("PB_APP: Opening xlsx workbook.")
        workbook = Workbook(f"/storage/emulated/0/documents/{date}.xslx")

        Logger.info("PB_APP: Starting to write to workbook.")
        for org in orgs:
            donations = self.get_organization_donations(org.id)
            if not donations:
                # there is nothing so skip
                continue

            worksheet = workbook.add_worksheet(org.name)
            Logger.info(f"PB_APP: writing donations of org: `{org.name}` to workbook.")
            for i, donation in enumerate(donations):
                worksheet.write(i, 0, donation[0])
                worksheet.write(i, 1, donation[1])
                worksheet.write(i, 2, donation[2])

        Logger.info("PB_APP: Finished writing to workbook, closing now.")
        workbook.close()
