import sqlite3
import pandas as pd

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
        # self.cur.execute(f"SELECT obchod, typ, SUM(vaha) FROM {org} GROUP BY obchod, typ;")
        # amount = self.cur.fetchall()
        # self.conn.commit()
        amount = pd.read_sql_query(f'SELECT obchod, typ, SUM(vaha) FROM {org} GROUP BY obchod, typ;', self.conn)
        return amount

    def org_list(self):
        self.cur.execute("SELECT name FROM sqlite_master where type='table';")
        tup_names = self.cur.fetchall()
        self.conn.commit()
        names = [i for tup in tup_names for i in tup]
        names.remove("sqlite_sequence")
        return names
