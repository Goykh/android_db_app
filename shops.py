import sqlite3


class Organisation:
    def __init__(self, name):
        self.conn = sqlite3.connect("pb.db")
        self.cur = self.conn.cursor()
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {name}"
                         f" (id INTEGER PRIMARY KEY,"
                         f"obchod TEXT, "
                         f"typ_A TEXT,"
                         f"typ_B TEXT,"
                         f"typ_C TEXT,"
                         f"vaha INT,"
                         f"datum TEXT)")
        self.conn.commit()

    def insert(self, org, shop, type, amount):
        if type.upper() == "A":
            self.cur.execute(
                f'INSERT INTO {org}(obchod, typ_A, vaha, datum) VALUES(?, 1, ?, datetime("now", "localtime"))',
                (shop, amount))
        elif type.upper() == "B":
            self.cur.execute(
                f'INSERT INTO {org}(obchod, typ_B, vaha, datum) VALUES(?, 1, ?, datetime("now", "localtime"))',
                (shop, amount))
        elif type.upper() == "C":
            self.cur.execute(
                f'INSERT INTO {org}(obchod, typ_C, vaha, datum) VALUES(?, 1, ?, datetime("now", "localtime"))',
                (shop, amount))
        self.conn.commit()

    def get_type_amount(self, org, shop, type):
        if type.upper() == "A":
            self.cur.execute(f"SELECT SUM(vaha) FROM {org} WHERE obchod='{shop}' AND typ_A=1")
            amount = self.cur.fetchone()
            self.conn.commit()
            return amount

        elif type.upper() == "B":
            self.cur.execute(f"SELECT SUM(vaha) FROM {org} WHERE obchod='{shop}' AND typ_B=1")
            amount = self.cur.fetchone()
            self.conn.commit()
            return amount

        elif type.upper() == "C":
            self.cur.execute(f"SELECT SUM(vaha) FROM {org} WHERE obchod='{shop}' AND typ_A=1")
            amount = self.cur.fetchone()
            self.conn.commit()
            return amount
