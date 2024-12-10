import tkinter as tk
from tkinter import messagebox, ttk
from db_connection import DbConnection
from Detail import Detail


class Order:
    header = ["Идентификатор", "Идентификатор покупателя", "Статус", "Идентификатор сборщика", "Дата создания", "Дата выдачи"]
    content = []
    button_mas = []

    @staticmethod
    def get_data():
        Order.content.clear()
        query = f"SELECT * FROM Заказы;"
        DbConnection.cursor.execute(query)
        Order.content = DbConnection.cursor.fetchall()


    @staticmethod
    def show_data(scrollable_frame):

        Order.get_data()

        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        len_title = len(Order.header)
        title = tk.Label(scrollable_frame, text="Заказы", fg="black", font=("Impact", 20))
        title.grid(row=0, column=0, columnspan=len_title, sticky='ew', padx=10, pady=25)


        label_h1 = tk.Label(scrollable_frame, text="Идентификатор", fg="black", font=("Arial", 16, "bold"))
        label_h1.grid(row=1, column=0, sticky='nsew', padx=10)

        label_h2 = tk.Label(scrollable_frame, text="Статус", fg="black", font=("Arial", 16, "bold"))
        label_h2.grid(row=1, column=1, sticky='nsew', padx=10)

        for index_row, rows in enumerate(Order.content, start=0):
            Order.button_mas.append([])

            label_id = tk.Label(scrollable_frame, text=rows[0], fg="black", font=("Arial", 14))
            label_id.grid(row=index_row + 2, column=0, sticky='nsew')

            label_status = tk.Label(scrollable_frame, text=rows[2], fg="black", font=("Arial", 14))
            label_status.grid(row=index_row + 2, column=1, sticky='nsew')

            button_detail = tk.Button(scrollable_frame, text="Подробнее", command=lambda p1=rows: Detail.show_data(scrollable_frame, p1))
            button_detail.grid(row=index_row + 2, column=2, sticky='nsew')

            Order.button_mas[index_row].append(label_id)
            Order.button_mas[index_row].append(label_status)