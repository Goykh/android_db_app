import sqlite3
from xlsxwriter.workbook import Workbook


class Organisation:
    def __init__(self, name):
        """
        Connects to the db, creates the table if it doesn't exist (it should).
        :param name: name of db table
        """
        self.conn = sqlite3.connect("pd2.db")
        self.cur = self.conn.cursor()
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {name}"
                         f" (id INTEGER PRIMARY KEY,"
                         f"obchod TEXT,"
                         f"typ TEXT,"
                         f"vaha INT,"
                         f"datum TEXT);")
        self.conn.commit()

    def insert(self, org, shop, type, amount):
        """
        Inserts data into a table.
        Input comes from the Kivy buttons.
        Also adds a date
        :param org: name of the org -> table name
        :param shop: name of the shop
        :param type: type of the food (A, B, C, M)
        :param amount: amount of food
        """
        self.cur.execute(
            f'INSERT INTO {org}(obchod, typ, vaha, datum) VALUES(?, ?, ?, datetime("now", "localtime"));',
            (shop, type.upper(), amount))
        self.conn.commit()

    def get_type_amount(self, org):
        """
        Gets the amount of food by type from the DB
        :param org: org name -> table name
        :return: the amount grouped by shop name and type
        """

        self.cur.execute(f"SELECT obchod, typ, SUM(vaha), datum FROM {org} GROUP BY obchod, typ;")
        amount = self.cur.fetchall()
        self.conn.commit()
        return amount

    def org_list(self):
        """
        This method is used to create the buttons.
        Makes a list out of all table names.
        :return: list with table names
        """
        self.cur.execute("SELECT name FROM sqlite_master where type='table';")
        tup_names = self.cur.fetchall()
        self.conn.commit()
        names = [i for tup in tup_names for i in tup]
        names.remove("sqlite_sequence")
        return names

    # TODO: Method to delete records (probably delete all and you can do it manually every month)

    # TODO: try to come up with a solution to export the db to a csv file
    def to_csv_file(self, org):
        """
        CURRENTLY NOT USED, BUT WILL BE IN THE FUTURE!
        Puts data from the SQL table into a csv file.
        :param org: org name -> table name
        :return: csv file with the data
        """
        workbook = Workbook(f'{org}.xlsx')
        worksheet = workbook.add_worksheet()
        data = self.cur.execute(f'SELECT obchod, typ, SUM(vaha) FROM {org} GROUP BY obchod, typ;')
        for i, row in enumerate(data):
            print(row)
            worksheet.write(i, 0, row[0])
            worksheet.write(i, 1, row[1])
            worksheet.write(i, 2, row[2])
        workbook.close()
