import sqlite3
from xlsxwriter.workbook import Workbook

class Organisation:
    def __init__(self, name):
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
        self.cur.execute(
            f'INSERT INTO {org}(obchod, typ, vaha, datum) VALUES(?, ?, ?, datetime("now", "localtime"));',
            (shop, type.upper(), amount))
        self.conn.commit()

    def get_type_amount(self, org):
        self.cur.execute(f"SELECT obchod, typ, SUM(vaha), datum FROM {org} GROUP BY obchod, typ;")
        amount = self.cur.fetchall()
        self.conn.commit()
        return amount

    def org_list(self):
        self.cur.execute("SELECT name FROM sqlite_master where type='table';")
        tup_names = self.cur.fetchall()
        self.conn.commit()
        names = [i for tup in tup_names for i in tup]
        names.remove("sqlite_sequence")
        return names

    # TODO: Method to delete records (probably delete all and you can do it manually every month)

    # TODO: try to come up with a solution to export the db to a csv file
    def to_csv_file(self, org):
        workbook = Workbook(f'{org}.xlsx')
        worksheet = workbook.add_worksheet()
        data = self.cur.execute(f'SELECT obchod, typ, SUM(vaha) FROM {org} GROUP BY obchod, typ;')
        for i, row in enumerate(data):
            print(row)
            worksheet.write(i, 0, row[0])
            worksheet.write(i, 1, row[1])
            worksheet.write(i, 2, row[2])
        workbook.close()