import pyodbc
import sys
import tkinter as tk

from db_connection import DbConnection
from Init_root import InitRoot

try:
    conn = DbConnection.connect_to_access_db(r'C:\Users\Андрей\Desktop\Совместные проекты\КПО\DB.accdb')
    print("Подключение к базе данных успешно!")
except pyodbc.Error as ex:
    print("Ошибка подключения к базе данных: ", ex)
    sys.exit()


master = tk.Tk()
master.title("Система магазина")

first_entry = tk.Entry(master, width=20, font='ComicSans 18')
second_entry = tk.Entry(master, width=20, font='ComicSans 18')

first_entry.pack(anchor='w', padx=10, pady=25)
second_entry.pack(anchor='w', padx=10, pady=25)
sign_in_button = tk.Button(master, text="Войти", width=4, height=2, font='ComicSans 18',
                           command=lambda p1=first_entry, p2=second_entry: InitRoot.initial(master, p1, p2))
sign_in_button.pack(anchor='center', padx=10, pady=25)

master.attributes("-topmost", True)
master.mainloop()


DbConnection.close_connection()

