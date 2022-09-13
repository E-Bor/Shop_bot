import platform
import sqlite3
import os
import subprocess
import datetime
import platform

from unicodedata import category

from bot_logger.BotLogger import logger


class DatabaseControll:
    """class that need for working with database"""

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.path = os.path.dirname(os.path.abspath(__file__))+"\\" + self.db_name if platform.system() == "Windows" \
            else os.path.dirname(os.path.abspath(__file__))+"/" + self.db_name

    # create connection with db that named db_name
    def create_connection(self):
        try:
            sqlite_connection = sqlite3.connect(str(self.path))
            cursor = sqlite_connection.cursor()
            logger.info("База данных создана и успешно подключена к SQLite")
            return cursor, sqlite_connection

        except sqlite3.Error as error:
            logger.info(f"Ошибка при подключении к sqlite {error}")

    # stop connection with database
    def stop_connection(self, sqlite_connection):
        if sqlite_connection:
            sqlite_connection.close()
            logger.info("Соединение с SQLite закрыто")

    # read data from database
    def read_data(self, category):
        logger.info(f"Calles function to read data from db with category: '{category}'")
        cur, con = self.create_connection()
        sql_request = "select * from files where category=:category"
        data = cur.execute(sql_request, {"category": category}).fetchall()
        self.stop_connection(con)
        return data

    # add position to database
    def add_position(self, *args):
        logger.info(f"Calles function to add data from db: '{args}'")
        cur, con = self.create_connection()
        sql_request = "insert into files values (?,?,?,?,?,?)"
        cur.execute(sql_request, args)
        con.commit()
        self.stop_connection(con)

    # edit position in database
    def edit_position(self, category, item, value):
        logger.info(f"Calles function to edit data from db with , category: '{category}'")
        cur, con = self.create_connection()
        if len(self.read_data(category)) == 0:
            logger.info(f"Not correct category '{category}' ")
        else:
            try:
                sql_request = f"update files set {item} = ? where category= ?"
                cur.execute(sql_request, (value, category,))
                con.commit()
            except sqlite3.OperationalError:
                logger.info(f" no such collumn with name {item}")
        self.stop_connection(con)

    # delete position in database
    def delete_position(self, category):
        logger.info(f"Calles function to delete data from db with category: '{category}'")
        cur, con = self.create_connection()
        sql_request = "DELETE FROM files  where category like ?"
        cur.execute(sql_request, ("{}%".format(category),))
        con.commit()

    # add record with new user
    def register_new_user(self, user_id):
        logger.info("registrated new user")
        cur, con = self.create_connection()
        print(datetime.date.today())
        sql_request = "insert into stats_user values (?,?)"
        cur.execute(sql_request, (user_id, datetime.date.today()))
        con.commit()

    # check users in date interval (start,stop)
    def check_new_users(self, start, stop):
        logger.info(f"check new users for the period: {start} --- {stop}")
        cur, con = self.create_connection()
        sql_request = "SELECT COUNT(*) FROM stats_user WHERE `reg_time` >= ? and `reg_time` <= ?"
        amount = cur.execute(sql_request, (str(start), str(stop))).fetchone()
        return amount[0]

    # add position about new buy in database
    def register_new_buy(self, cat):
        logger.info("registrated new buy")
        cur, con = self.create_connection()
        sql_request = "insert into stats_shoping values (?,?)"
        cur.execute(sql_request, (cat, datetime.date.today()))
        con.commit()

    # check purchase in date interval (start, stop)
    def check_purchases(self, cat, start, stop):
        logger.info(f"check new purchases for the period: {start} --- {stop}")
        cur, con = self.create_connection()
        sql_request = "SELECT COUNT(*) FROM stats_shoping WHERE category LIKE ? and `date` >= ? and `date` <= ?"
        amount = cur.execute(sql_request, ("{}%".format(cat),start,stop)).fetchone()
        return amount[0]

    # creating backup database
    def backup(self):
        cur, con = self.create_connection()
        path = os.path.dirname(os.path.abspath(__file__))+"\\" + "backup.db" if platform.system() == "Windows" \
            else os.path.dirname(os.path.abspath(__file__))+"/" + "backup.db"
        backup = sqlite3.connect(str(path))
        with backup:
            con.backup(backup, pages=0)
        backup.close()
        pass


database = DatabaseControll("filesdata.db")


# date format "2022-08-22"
