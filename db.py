import sqlite3 as sq
import os.path
from typing import List

from datetime import date
from parse import Parse



def connection_wrapper(func):
    def inner(*args):
        conn = sq.connect(database='/home/a0999441/domains/parcingcbscript.ru/public_html/data/database.db')
        cursor = conn.cursor()
        result = func(*args, cursor=cursor, conn=conn)
        cursor.close()
        conn.close()
        return result
    return inner



class DB:

    @staticmethod
    def __currencies_list(currencies: str) -> List[str]:
        return currencies.split(', ')



    @staticmethod
    def __rewriting_db_cost() -> None:
        if not os.path.exists(f'/home/a0999441/domains/parcingcbscript.ru/public_html/data/sites/{date.today()}.html'):
            table = Parse.get_currency_table()
            DB.write_currency_table(table)



    @staticmethod
    @connection_wrapper
    def write_user_info(user_id: str, currencies: str, notification_time: str, cursor, conn) -> None:
        cursor.execute("""DELETE FROM Users WHERE User_id = ?""", (user_id,))
        cursor.execute("""INSERT INTO Users VALUES (?, ?, ?)""",
                       (user_id, currencies, notification_time))
        conn.commit()



    @staticmethod
    @connection_wrapper
    def set_notification_time(user_id: str, notification_time: str,  cursor, conn) -> None:
        cursor.execute("""UPDATE Users SET NotificationTime = ? WHERE User_id = ?""", (notification_time, user_id))
        conn.commit()



    @staticmethod
    @connection_wrapper
    def set_currencies(user_id: str, currencies: str, cursor, conn) -> None:
        cursor.execute("""UPDATE Users SET Currencies = ? WHERE User_id = ?""", (currencies, user_id))
        conn.commit()



    @staticmethod
    @connection_wrapper
    def get_currencies(user_id: str, cursor, conn) -> str:
        cursor.execute("""SELECT Currencies FROM Users WHERE User_id = ?""", (user_id,))
        return cursor.fetchone()[0]



    @staticmethod
    @connection_wrapper
    def get_notification_time(user_id: str, cursor, conn) -> str:
        cursor.execute("""SELECT NotificationTime FROM Users WHERE User_id = ?""", (user_id,))
        return cursor.fetchone()[0]




    @classmethod
    @connection_wrapper
    def get_currencies_cost(cls, user_id: str, cursor, conn) -> str:
        cls.__rewriting_db_cost()

        currencies = cls.get_currencies(user_id)

        currencies_list = cls.__currencies_list(currencies)
        result = ''

        for currency in currencies_list:
            cursor.execute("""SELECT Cost FROM Cost WHERE Name = ?""", (currency,))
            cost = cursor.fetchone()[0]
            result += f'{currency}: {cost}' + '\n'

        return result



    @staticmethod
    @connection_wrapper
    def write_currency_table(python_table: List[List], cursor, conn) -> None:
        cursor.execute("""DELETE FROM Cost""")

        for line in python_table:
            cursor.execute("""INSERT INTO Cost
            VALUES (?, ?)""", (line[0], line[1]))
            conn.commit()



    @classmethod
    @connection_wrapper
    def check_correct_currencies(cls, currencies: str, cursor, conn) -> bool:
        cls.__rewriting_db_cost()

        currencies_list = cls.__currencies_list(currencies)

        cursor.execute("""SELECT Name FROM Cost""")
        all_possible_currencies = set(cursor.fetchall())

        return all((currency,) in all_possible_currencies for currency in currencies_list)
