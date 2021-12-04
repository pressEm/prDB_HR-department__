import datetime
import math
import sqlite3
import time


class FDataBase:

    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_all_emplyee(self):
        try:
            self.__cur.execute(
                f"SELECT * FROM employee")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения из БД" + str(e))
        return False

    def get_employee(self, id):
        print("get_employee")
        print(id)
        try:
            self.__cur.execute(
                f"SELECT * FROM employee where id == :id", (id,))
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения из БД" + str(e))
        return False

    def get_all_offices(self):
        try:
            self.__cur.execute(
                f"SELECT * FROM office")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения из БД" + str(e))
        return False

    def get_all_posts(self):
        try:
            self.__cur.execute(
                f"SELECT * FROM post")
            # f"select * from sqlite_master where type = 'table'")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения из БД" + str(e))
        return False

    def get_all_records(self):
        try:
            self.__cur.execute(
                f"SELECT * FROM work_record")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения из БД" + str(e))
        return False

    def get_records_by_office(self, id):
        print(id)
        try:
            self.__cur.execute(
                f"SELECT * FROM work_record where office_code==:id", (id,))
            res = self.__cur.fetchall()
            print(len(res))
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения из БД" + str(e))
        return False

    def get_records_by_post(self, id):
        print(id)
        try:
            self.__cur.execute(
                f"SELECT * FROM work_record where post_code==:id", (id,))
            res = self.__cur.fetchall()
            print(len(res))
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения из БД" + str(e))
        return False


    def add_employee(self, name, surname, email, address, post_code, office_code):
        try:
            date_ = datetime.datetime.now()
            print(date_)
            sql = """INSERT INTO employee (name, surname, email, home_address, date_of_last_changes)
                      values (:name, :surname, :email, :home_address, :date_of_last_changes)"""
            self.__cur.execute(sql, [name, surname, email, address, date_])
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БДLL " + str(e))
            return False
        self.__cur.execute(f"SELECT * FROM employee where date_of_last_changes == :date_", [date_])
        res = self.__cur.fetchone()
        print(res[0])
        self.add_record(res[0], post_code, office_code, res[5])
        return True

    def add_record(self, id_emp, post_code, office_code, start_date):
        print(id_emp)
        try:
            sql = """INSERT INTO work_record (id_employee, post_code, office_code, start_date)
                      values (:id_emp, :post_code, :office_code, :start_date)"""
            self.__cur.execute(sql, [id_emp, post_code, office_code, start_date])
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False
        return True

    def add_post(self, title, duties):
        try:
            sql = """INSERT INTO post (title, Duties)
                                 values (:title, :duties)"""
            self.__cur.execute(sql, [title, duties])
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False
        return True

    def add_office(self, address, phone_number):
        try:
            sql = """INSERT INTO office (address, phone_number)
                                            values (:address, :phone_number)"""
            self.__cur.execute(sql, [address, phone_number])
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False
        return True

    def update_employee(self, id, name, surname, email, address):
        try:
            date_ = datetime.datetime.now()
            sql = """UPDATE employee SET name=:name, surname=:surname, email=:email, 
            home_address=:home_address, date_of_last_changes=:date_of_last_changes where id=:id"""
            # sql = """INSERT INTO employee (name, surname, email, home_address, date_of_last_changes)
            #              values (:name, :surname, :email, :home_address, :date_of_last_changes)"""
            self.__cur.execute(sql, [name, surname, email, address, date_, id])
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БДLL " + str(e))
            return False
        self.__cur.execute(f"SELECT * FROM employee where date_of_last_changes == :date_", [date_])
        res = self.__cur.fetchone()
        print(res[0])
        # self.add_record(res[0], post_code, office_code, res[5])
        return True

    def update_employee(self, id, name, surname, email, address):
        try:
            date_ = datetime.datetime.now()
            self.__cur.execute(f"SELECT date_of_last_changes FROM employee where id == :id", (id,))
            start_date = self.__cur.fetchone()
            print(start_date[0])
            sql = """UPDATE employee SET name=:name, surname=:surname, email=:email, 
            home_address=:home_address, date_of_last_changes=:date_of_last_changes where id=:id"""
            self.__cur.execute(sql, [name, surname, email, address, date_, id])
            self.__db.commit()
            self.create_hist_rec(id, start_date[0], date_, surname, email, address)
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БДLL " + str(e))
            return False
        self.__cur.execute(f"SELECT * FROM employee where date_of_last_changes == :date_", [date_])
        res = self.__cur.fetchone()
        print(res[0])
        # self.add_record(res[0], post_code, office_code, res[5])
        return True
    def create_hist_rec(self, id_employee, start_date, finish_date, surname, email, home_address):
        try:
            sql = """INSERT INTO history_of_changes (id_employee, start_date, finish_date, surname, email, home_address)
                                                   values (:id_employee, :start_date, :finish_date, :surname, :email, :home_address)"""
            self.__cur.execute(sql, [id_employee, start_date, finish_date, surname, email, home_address])
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False
        return True
    def delete_employee(self, idd):
        date_ = datetime.datetime.now()
        try:
            self.__cur.execute(f"UPDATE work_record SET finish_date = :date_ where id_employee == :idd", (date_, idd,))
            sql1 = """DELETE FROM employee WHERE id == :idd"""
            self.__cur.execute(sql1, (idd,))
            self.__db.commit()
            res = self.__cur.fetchone()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка при удалении комментария из БД " + str(e))
        return False

    def set_finish_date(self, id_, date_):
        try:
            sql = """UPDATE work_record SET finish_date=:date_ where id_employee == :id_"""
            self.__cur.execute(sql, (date_, id_))
            self.__db.commit()
            res = self.__cur.fetchone()

        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False

    def delete_office(self, code):
        try:
            sql = """DELETE FROM office WHERE code == :code"""
            self.__cur.execute(sql, [code])
            self.__db.commit()
            res = self.__cur.fetchone()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка при удалении комментария из БД " + str(e))
        return False

    def delete_post(self, code):
        try:
            sql = """DELETE FROM post WHERE code == :code"""
            self.__cur.execute(sql, [code])
            self.__db.commit()
            res = self.__cur.fetchone()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка при удалении комментария из БД " + str(e))
        return False
