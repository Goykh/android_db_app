import sqlite3

from xlsxwriter.workbook import Workbook



class Organisation:
    def __init__(self, name):
        """
        Connects to the db, creates the table if it doesn't exist (it should).
        :param name: name of db table
        """
        if ' ' in name:
            name = name.replace(' ', '_')
        self.conn = sqlite3.connect("pd2.db")
        self.cur = self.conn.cursor()
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {name}"
                         f" (id INTEGER PRIMARY KEY,"
                         f"obchod TEXT,"
                         f"typ TEXT,"
                         f"vaha INT,"
                         f"datum TEXT);")
        self.conn.commit()

    def insert(self, org, shop, food_type, amount):
        """
        Inserts data into a table.
        Input comes from the Kivy buttons.
        Also adds a date
        :param org: name of the org -> table name
        :param shop: name of the shop
        :param food_type: type of the food (A, B, C, M)
        :param amount: amount of food
        """
        if ' ' in org:
            org = org.replace(' ', '_')

        self.cur.execute(
            f'INSERT INTO {org}(obchod, typ, vaha, datum) VALUES(?, ?, ?, datetime("now", "localtime"));',
            (shop, food_type.upper(), amount))
        self.conn.commit()

    def get_type_amount(self, org):
        """
        Gets the amount of food by type from the DB
        :param org: org name -> table name
        :return: the amount grouped by shop name and type
        """
        if ' ' in org:
            org = org.replace(' ', '_')
        self.cur.execute(f"SELECT obchod, typ, SUM(vaha), datum FROM {org} GROUP BY obchod, typ;")
        amount = self.cur.fetchall()
        self.conn.commit()
        return amount

    def get_all_table_data(self, org):
        """
        Gets all entries in a table.
        :param org: org name -> table name
        """
        if ' ' in org:
            org = org.replace(' ', '_')
        self.cur.execute(f"SELECT * FROM {org};")
        data = self.cur.fetchall()
        self.conn.commit()
        return data

    # SNIPPET TO CONVERT DATETIME FROM SQL INTO ONLY DATE
    # 4th index in tuple
    # date[:10] - gives date in YYYY-MM-DD
    # date = f"{date[8:]}-{date[5:7]}-{date[:4]}" - reverse DD-MM-YYYY

    def org_list(self):
        """
        This method is used to create the buttons.
        Makes a list out of all table names.
        :return: list with table names
        """
        self.cur.execute("SELECT name FROM sqlite_master where type='table';")
        tup_names = self.cur.fetchall()
        self.conn.commit()
        names_raw = [i for tup in tup_names for i in tup]
        names_raw.remove("sqlite_sequence")
        names = []
        for name in names_raw:
            if '_' in name:
                new_name = name.replace('_', ' ')
                names.append(new_name)
            else:
                names.append(name)
        names.sort()
        return names

    def delete_data_in_table(self, org):
        """
        For now, deletes all data from table.
        In the future, maybe add an option
        to delete from and until certain date.
        :param org: org name -> table name
        """
        if ' ' in org:
            org = org.replace(' ', '_')
        self.cur.execute(f"DELETE FROM {org};")
        self.conn.commit()

    def to_xlsx_file(self, org, path):
        """
        CURRENTLY NOT USED, BUT WILL BE IN THE FUTURE!
        Puts data from the SQL table into a csv file.
        :param org: org name -> table name
        :return: csv file with the data
        """
        if ' ' in org:
            org = org.replace(' ', '_')
        workbook = Workbook(f'{path}/{org}.xlsx')
        worksheet = workbook.add_worksheet()
        data = self.cur.execute(f'SELECT obchod, typ, SUM(vaha) FROM {org} GROUP BY obchod, typ;')
        for i, row in enumerate(data):
            worksheet.write(i, 0, row[0])
            worksheet.write(i, 1, row[1])
            worksheet.write(i, 2, row[2])
        workbook.close()
