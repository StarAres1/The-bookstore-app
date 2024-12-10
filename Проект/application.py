import pyodbc
import sys
import tkinter as tk

from db_connection import DbConnection
from Init_root import InitRoot


class Main:
    def __init__(self, root):
        self.master = root
        conn = DbConnection.connect_to_access_db(r'C:\Users\User\PycharmProjects\BookStoreByTI\DB.accdb')
        if conn:
            print("Подключение к базе данных успешно!")
        else:
            print("Ошибка подключения к базе данных: ")
            sys.exit()
        print("Запуск")
        to_print = self.start()
        print(to_print)
        return

    def start(self):

        self.master.title("Система магазина")

        first_entry = tk.Entry(self.master, width=20, font='ComicSans 18')
        second_entry = tk.Entry(self.master, width=20, font='ComicSans 18')

        first_entry.pack(anchor='w', padx=10, pady=25)
        second_entry.pack(anchor='w', padx=10, pady=25)
        sign_in_button = tk.Button(self.master, text="Войти", width=4, height=2, font='ComicSans 18',
                                   command=lambda p1=first_entry, p2=second_entry: InitRoot.initial(self.master, p1, p2))
        sign_in_button.pack(anchor='center', padx=10, pady=25)

        self.master.attributes("-topmost", True)
        print("Интерфейс настроен")
        return True


approot = tk.Tk()
App = Main(approot)
approot.mainloop()
DbConnection.close_connection()
