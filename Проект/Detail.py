import tkinter as tk
from db_connection import DbConnection
from datetime import datetime


class Detail:
    header = ["Идентификатор", "Фамилия", "Имя", "Отчество", "Страна"]
    content_buyer = []
    content_order = []
    content_details = []
    button_mas = []

    @staticmethod
    def get_data(data_of_order):
        Detail.content_buyer = []
        Detail.content_order = []
        Detail.content_details = []

        query = f"SELECT [Идентификатор товара], Количество, Цена FROM [Детали заказа] WHERE [Идентификатор заказа] = {data_of_order[0]};"
        DbConnection.cursor.execute(query)
        Detail.content_details = DbConnection.cursor.fetchall()

        query = f"SELECT Фамилия, Имя, [Дата рождения], [Номер телефона] FROM Клиенты WHERE [Идентификатор] = {data_of_order[1]};"
        DbConnection.cursor.execute(query)
        Detail.content_buyer = DbConnection.cursor.fetchall()

        Detail.content_order = data_of_order

    @staticmethod
    def cancel(label):
        key = Detail.content_order[0]
        mas_detail = Detail.content_details
        for element in mas_detail:
            query = "SELECT Количество FROM Книги WHERE ISBN = ?;"
            DbConnection.cursor.execute(query, (element[0],))
            number = DbConnection.cursor.fetchone()[0]

            query = (f"UPDATE Книги "
                     f"SET Количество = ? "
                     f"WHERE ISBN = ?")
            DbConnection.cursor.execute(query, (number + element[1], element[0]))

        query = (f"UPDATE Заказы "
                 f"SET Статус = ? "
                 f"WHERE Идентификатор = ?")
        DbConnection.cursor.execute(query, ("Отменен", key))

        label.config(text="Отменен")
        DbConnection.commit()

    @staticmethod
    def high(label1, label2):
        if label1.cget("text") == "Создан":
            label1.config(text="Собран")

            query = (f"UPDATE Заказы "
                     f"SET Статус = ? "
                     f"WHERE Идентификатор = ?")
            DbConnection.cursor.execute(query, ("Собран", Detail.content_order[0]))

        elif label1.cget("text") == "Собран":
            label1.config(text="Выдан")
            label2.config(text=datetime.now())
            query = (f"UPDATE Заказы "
                     f"SET Статус = ? "
                     f"WHERE Идентификатор = ?")
            DbConnection.cursor.execute(query, ("Выдан", Detail.content_order[0]))

            query = (f"UPDATE Заказы "
                     f"SET [Дата выдачи] = ? "
                     f"WHERE Идентификатор = ?")
            DbConnection.cursor.execute(query, (datetime.now(), Detail.content_order[0]))

        DbConnection.commit()


    @staticmethod
    def show_data(scrollable_frame, data_of_order):

        Detail.get_data(data_of_order)

        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        len_title = len(Detail.header)
        title = tk.Label(scrollable_frame, text=f"Заказ N{data_of_order[0]}", fg="black", font=("Impact", 25))
        title.grid(row=0, column=0, columnspan=len_title, sticky='W', padx=10, pady=25)

        label_info_buyer = tk.Label(scrollable_frame, text="Информация о покупателе", fg="black", font=("Arial", 18, "bold", "underline"))
        label_info_buyer.grid(row=1, column=0, columnspan=len_title, sticky='W', padx=10)

        label_surname_buyer1 = tk.Label(scrollable_frame, text="Фамилия:", fg="black", font=("Arial", 16))
        label_surname_buyer1.grid(row=2, column=0, sticky='W', padx=10)

        label_surname_buyer2 = tk.Label(scrollable_frame, text=Detail.content_buyer[0][0], fg="black", font=("Arial", 16))
        label_surname_buyer2.grid(row=2, column=1, sticky='W', padx=10)

        label_name_buyer1 = tk.Label(scrollable_frame, text="Имя:", fg="black", font=("Arial", 16))
        label_name_buyer1.grid(row=3, column=0, sticky='W', padx=10)

        label_name_buyer2 = tk.Label(scrollable_frame, text=Detail.content_buyer[0][1], fg="black", font=("Arial", 16))
        label_name_buyer2.grid(row=3, column=1, sticky='W', padx=10)

        label_number_buyer1 = tk.Label(scrollable_frame, text="Номер телефона: ", fg="black", font=("Arial", 16))
        label_number_buyer1.grid(row=4, column=0, sticky='W', padx=10)

        label_number_buyer2 = tk.Label(scrollable_frame, text=Detail.content_buyer[0][3], fg="black", font=("Arial", 16))
        label_number_buyer2.grid(row=4, column=1, sticky='W', padx=10)

        label_birth_buyer1 = tk.Label(scrollable_frame, text="Дата рождения:", fg="black", font=("Arial", 16))
        label_birth_buyer1.grid(row=5, column=0, sticky='W', padx=10)

        label_birth_buyer2 = tk.Label(scrollable_frame, text=Detail.content_buyer[0][2], fg="black", font=("Arial", 16))
        label_birth_buyer2.grid(row=5, column=1, sticky='W', padx=10)

        label_info_buyer = tk.Label(scrollable_frame, text="Состав заказа", fg="black", font=("Arial", 18, "bold", "underline"))
        label_info_buyer.grid(row=6, column=0, columnspan=len_title, sticky='W', padx=10)

        label_info_buyer = tk.Label(scrollable_frame, text="Идентификатор товара", fg="black", font=("Arial", 16, "bold"))
        label_info_buyer.grid(row=7, column=0, sticky='W', padx=10)

        label_info_buyer = tk.Label(scrollable_frame, text="Количество", fg="black", font=("Arial", 16, "bold"))
        label_info_buyer.grid(row=7, column=1, columnspan=len_title, sticky='W', padx=10)

        label_info_buyer = tk.Label(scrollable_frame, text="Цена", fg="black", font=("Arial", 16, "bold"))
        label_info_buyer.grid(row=7, column=2, columnspan=len_title, sticky='W', padx=10)

        for index_row, row in enumerate(Detail.content_details, start=0):
            for index_column, element in enumerate(row, start=0):
                label_birth_buyer2 = tk.Label(scrollable_frame, text=element, fg="black", font=("Arial", 16))
                label_birth_buyer2.grid(row=index_row + 8, column=index_column, sticky='W', padx=10)

        next_row = len(Detail.content_details) + 8
        summa = 0

        for i in Detail.content_details:
            summa += i[2] * i[1]

        label_itog = tk.Label(scrollable_frame, text=f"Итог: {summa}", fg="black", font=("Arial", 16, "bold"))
        label_itog.grid(row=next_row, column=2, columnspan=len_title, sticky='W', padx=10)

        label_info_buyer = tk.Label(scrollable_frame, text="Информация о сборе заказа", fg="black", font=("Arial", 18, "bold", "underline"))
        label_info_buyer.grid(row=next_row + 1, column=0, columnspan=len_title, sticky='W', padx=10)

        label_status1 = tk.Label(scrollable_frame, text="Статус", fg="black", font=("Arial", 16, "bold"))
        label_status1.grid(row=next_row + 2, column=0, sticky='W', padx=10)

        label_status2 = tk.Label(scrollable_frame, text=Detail.content_order[2], fg="black", font=("Arial", 16, "bold"))
        label_status2.grid(row=next_row + 2, column=1, columnspan=len_title, sticky='W', padx=10)

        label_collect1 = tk.Label(scrollable_frame, text="Сборщик", fg="black", font=("Arial", 16, "bold"))
        label_collect1.grid(row=next_row + 3, column=0, sticky='W', padx=10)

        label_collect2 = tk.Label(scrollable_frame, text=Detail.content_order[3], fg="black", font=("Arial", 16, "bold"))
        label_collect2.grid(row=next_row + 3, column=1, columnspan=len_title, sticky='W', padx=10)

        label_date1 = tk.Label(scrollable_frame, text="Дата создания", fg="black", font=("Arial", 16, "bold"))
        label_date1.grid(row=next_row + 4, column=0, sticky='W', padx=10)

        label_date2 = tk.Label(scrollable_frame, text=Detail.content_order[4], fg="black", font=("Arial", 16, "bold"))
        label_date2.grid(row=next_row + 4, column=1, columnspan=len_title, sticky='W', padx=10)

        label_finish1 = tk.Label(scrollable_frame, text="Дата завершения", fg="black", font=("Arial", 16, "bold"))
        label_finish1.grid(row=next_row + 5, column=0, sticky='W', padx=10)

        label_finish2 = tk.Label(scrollable_frame, text=Detail.content_order[5], fg="black", font=("Arial", 16, "bold"))
        label_finish2.grid(row=next_row + 5, column=1, columnspan=len_title, sticky='W', padx=10)

        if label_status2.cget('text') != 'Отменен':
            if label_status2.cget("text") != 'Выдан':
                button_upgrade_status = tk.Button(scrollable_frame, text="Повысить статус",
                                          command=lambda p1=label_status2, p2=label_finish2: Detail.high(p1, p2))
                button_upgrade_status.grid(row=next_row + 2, column=2, sticky='E')

            button_upgrade_status = tk.Button(scrollable_frame, text="Отменить",
                                          command=lambda p1=label_status2: Detail.cancel(p1))
            button_upgrade_status.grid(row=next_row + 6, column=0, columnspan=3)