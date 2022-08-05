import sqlite3

from unicodedata import category

from bot_logger.BotLogger import logger

class DatabaseControll:
    def __init__(self,db_name:str):
        self.db_name = db_name

    def create_connection(self):
        try:
            sqlite_connection = sqlite3.connect(str(self.db_name))
            cursor = sqlite_connection.cursor()
            logger.info("База данных создана и успешно подключена к SQLite")
            return cursor,sqlite_connection
        except sqlite3.Error as error:
            logger.info(f"Ошибка при подключении к sqlite {error}")

    def stop_connection(self, sqlite_connection):
        if sqlite_connection:
            sqlite_connection.close()
            logger.info("Соединение с SQLite закрыто")

    def read_data(self, file_name, category):
        logger.info(f"Calles function to read data from db with filename: '{file_name}', category: '{category}'")
        cur,con = self.create_connection()
        sql_request = "select * from files where file_name=:filename and category=:category"
        data = cur.execute(sql_request, {"filename": file_name, "category": category}).fetchall()
        self.stop_connection(con)
        return data

    def add_position(self,*args):
        logger.info(f"Calles function to add data from db: '{args}'")
        cur, con = self.create_connection()
        sql_request = "insert into files values (?,?,?,?,?,?)"
        cur.execute(sql_request, args)
        con.commit()
        self.stop_connection(con)

    def edit_position(self, name, category, item, value):
        logger.info(f"Calles function to edit data from db with filename: '{name}', category: '{category}'")
        cur, con = self.create_connection()
        if len(self.read_data(name,category)) == 0:
            logger.info(f"Not correct name '{name}' or category '{category}' ")
        else:
            try:
                sql_request = f"update files set {item} = ? where file_name= ? and category= ?"
                cur.execute(sql_request, (value, name, category,))
                con.commit()
            except sqlite3.OperationalError:
                logger.info(f" no such collumn with name {item}")
        self.stop_connection(con)

    def delete_position(self, name, category):
        logger.info(f"Calles function to delete data from db with filename: '{name}', category: '{category}'")
        cur, con = self.create_connection()
        if len(self.read_data(name,category)) != 0:
            sql_request = "DELETE FROM files  where file_name= ? and category= ?"
            cur.execute(sql_request, (name, category))
            con.commit()


