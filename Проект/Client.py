import tkinter as tk
from tkinter import messagebox, ttk
from db_connection import DbConnection
import datetime


class Client:
    header = ["Идентификатор", "Стоимость купленных товаров", "Баллы", "Фамилия", "Имя", "Номер телефона", "Дата рождения"]
    content = []
    button_mas = []

    @staticmethod
    def get_data():
        Client.content.clear()
        query = f"SELECT * FROM Клиенты;"
        DbConnection.cursor.execute(query)
        Client.content = DbConnection.cursor.fetchall()

    @staticmethod
    def sql_delete(header, value, scrollable_frame, root):
        query = f"DELETE FROM Клиенты WHERE [{header}] = ?"
        try:
            DbConnection.cursor.execute(query, (value,))
            DbConnection.commit()
            messagebox.showinfo("Информация", "Запись успешно удалена!")
            Client.show_data(scrollable_frame, root)
        except Exception as e:
            messagebox.showwarning("Предупреждение", f"Непредвиденная ошибка: \n{e}\n\n")

    @staticmethod
    def validate(surname, name, number, birth, new_window, scrollable_frame, root):
        data = [surname.get(), name.get(), number.get(), birth.get()]
        error_message = "Ошибочный ввод: "
        is_error = False
        if not Client.validate_name(data[0]):
            error_message = error_message + "\nФамилия может содержать только буквы кириллицы, пробелы, дефисы, точки и апострофы"
            is_error = True
        if not Client.validate_name(data[1]):
            error_message = error_message + "\nИмя может содержать только буквы кириллицы, пробелы, дефисы, точки и апострофы"
            is_error = True
        if not Client.validate_number(data[2]):
            error_message = error_message + "\nВведите номер цифрами без разделителей."
            is_error = True
        if not Client.validate_date(data[3]):
            error_message = error_message + "\nДата может быть только в формате ГГГГ-ММ-ДД и должна быть раньше сегодняшнего дня."
            is_error = True
        if is_error:
            messagebox.showinfo("Ошибка ввода", message=error_message)
        else:
            Client.sql_add(data, new_window, scrollable_frame, root)

    @staticmethod
    def validate_id(id):
        try:
            id = int(id)
            if id > 0:
                return True
            return False
        except:
            return False


    @staticmethod
    def validate_name(name):
        alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        permitted_symbols = " -.'"
        for i in range(len(name)):
            if not (name[i] in alphabet or name[i] in alphabet.upper() or name[i] in permitted_symbols):
                return False
        return True

    @staticmethod
    def validate_number(number):
        try:
            number = int(number)
            if 10000000000 <= number < 10000000000000:
                return True
            else:
                return False
        except:
            return False


    @staticmethod
    def validate_date(date):
        date = date.split('-')
        if len(date) != 3:
            return False
        try:
            date[0] = int(date[0])
            date[1] = int(date[1])
            date[2] = int(date[2])
            date1 = datetime.date(year=date[0], month=date[1], day=date[2])
            if date1 > datetime.date.today():
                return False
            return True
        except:
            return False

    @staticmethod
    def validate_count(count):
        try:
            count = float(count)
            if count >= 0:
                return True
            return False
        except:
            return False

    @staticmethod
    def validate_amount(count):
        try:
            count = int(count)
            if count >= 0:
                return True
            return False
        except:
            return False

    @staticmethod
    def add_new_row(root, scrollable_frame):
        new_window = tk.Toplevel(root)
        new_window.title("Добавление")


        label_surname = ttk.Label(new_window, text="Фамилия:", font=("Arial", 14))
        label_surname.grid(row=0, column=0, sticky='nsew', pady=20)
        entry_surname = ttk.Entry(new_window)
        entry_surname.grid(row=0, column=1, sticky='nsew', pady=20, padx=10)

        label_name = ttk.Label(new_window, text="Имя:", font=("Arial", 14))
        label_name.grid(row=1, column=0, sticky='nsew', pady=20)
        entry_name = ttk.Entry(new_window)
        entry_name.grid(row=1, column=1, sticky='nsew', pady=20, padx=10)

        label_number = ttk.Label(new_window, text="Номер телефона:", font=("Arial", 14))
        label_number.grid(row=2, column=0, sticky='nsew', pady=20)
        entry_number = ttk.Entry(new_window)
        entry_number.grid(row=2, column=1, sticky='nsew', pady=20, padx=10)

        label_birth = ttk.Label(new_window, text="Дата рождения:", font=("Arial", 14))
        label_birth.grid(row=3, column=0, sticky='nsew', pady=20)
        entry_birth = ttk.Entry(new_window)
        entry_birth.grid(row=3, column=1, sticky='nsew', pady=20, padx=10)


        button = ttk.Button(new_window, text="Добавить",
                            command=lambda: Client.validate(entry_surname, entry_name, entry_number, entry_birth, new_window, scrollable_frame, root))
        button.grid(row=len(Client.header), column=0, columnspan=2, sticky='ew', padx=10, pady=25)


    @staticmethod
    def sql_add(data, new_window, scrollable_frame, root):
        try:
            query = f"INSERT INTO Клиенты (Фамилия, Имя, [Номер телефона], [Дата рождения]) VALUES (?, ?, ?, ?)"
            DbConnection.cursor.execute(query, data)
            DbConnection.commit()
            new_window.destroy()
            messagebox.showinfo("Информация", "Запись успешно добавлена!")
            Client.show_data(scrollable_frame, root)
        except Exception as e:
            messagebox.showwarning("Предупреждение",
                                       f"Непредвиденная ошибка: \n{e}\n\nПопробуйте ввести другие данные\n")
            new_window.lift()

    @staticmethod
    def update(key, value, change, root, scrollable_frame):
        new_window = tk.Toplevel(root)
        new_window.title("Редактирование")

        label = ttk.Label(new_window, text=f"Новое значение '{change}': ", font=("Arial", 14))
        label.grid(row=0, column=0, sticky='nsew', pady=25, padx=10)
        entry = ttk.Entry(new_window)
        entry.grid(row=0, column=1, sticky='nsew', pady=25, padx=10)
        button = ttk.Button(new_window, text="Обновить",
                            command=lambda: Client.sql_update(value, change, entry.get(), new_window, scrollable_frame, root))
        button.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=25)


    @staticmethod
    def sql_update(value, change, entry_value, new_window, scrollable_frame, root):
        query = f"UPDATE Клиенты " \
                f"SET [{change}] = ? " \
                f"WHERE [Идентификатор] = ? "
        if change == 'Идентификатор':
            if not Client.validate_id(entry_value):
                messagebox.showinfo("Ошибка ввода",
                                    message="Идентификатор должен быть целым положительным числом")
                return False
        elif change == 'Имя':
            if not Client.validate_name(entry_value):
                messagebox.showinfo("Ошибка ввода",
                                    message="Имя может содержать только буквы кириллицы, пробелы, дефисы, точки и апострофы.")
                return False
        elif change == 'Фамилия':
            if not Client.validate_name(entry_value):
                messagebox.showinfo("Ошибка ввода",
                                    message="Фамилия может содержать только буквы кириллицы, пробелы, дефисы, точки и апострофы.")
                return False
        elif change == 'Дата рождения':
            if not Client.validate_date(entry_value):
                messagebox.showinfo("Ошибка ввода",
                                    message="Дата может быть только в формате ГГГГ-ММ-ДД и должна быть раньше сегодняшнего дня.")
                return False
        elif change == 'Баллы':
            if not Client.validate_amount(entry_value):
                messagebox.showinfo("Ошибка ввода",
                                    message="Количество баллов выражается целым положительным числом.")
                return False
        elif change == 'Номер телефона':
            if not Client.validate_number(entry_value):
                messagebox.showinfo("Ошибка ввода",
                                    message="Введите номер цифрами без разделителей.")
                return False
        elif change == 'Стоимость купленных товаров':
            if not Client.validate_count(entry_value):
                messagebox.showinfo("Ошибка ввода",
                    message="Стоимость выражается положительной десятичной дробью.")
                return False
        try:
            DbConnection.cursor.execute(query, (entry_value, value))
            DbConnection.commit()
            new_window.destroy()
            messagebox.showinfo("Информация", "Запись успешно обновлена!")
            Client.show_data(scrollable_frame, root)
        except Exception as e:
            messagebox.showwarning("Предупреждение",
                                   f"Непредвиденная ошибка: \n{e}\n\nПопробуйте ввести другие данные\n")
            new_window.lift()

    @staticmethod
    def show_data(scrollable_frame, root):

        Client.get_data()

        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        len_title = len(Client.header)
        title = tk.Label(scrollable_frame, text="Клиенты", fg="black", font=("Impact", 20))
        title.grid(row=0, column=0, columnspan=len_title, sticky='ew', padx=10, pady=25)

        for index_column, element in enumerate(Client.header, start=0):
            label = tk.Label(scrollable_frame, text=element, fg="black", font=("Arial", 16, "bold"))
            label.grid(row=1, column=index_column, sticky='nsew', padx=10)


        for index_row, rows in enumerate(Client.content, start=0):
            Client.button_mas.append([])
            value = Client.content[index_row][0]
            for index_column, element in enumerate(rows, start=0):
                label = tk.Label(scrollable_frame, text=element, fg="black", cursor="hand2", font=("Arial", 14))
                label.grid(row=index_row + 2, column=index_column, sticky='nsew')
                label.bind("<Button-1>", lambda e, p1=Client.header[0], p2=value, p3=Client.header[index_column]: Client.update(p1, p2, p3, root, scrollable_frame))
                Client.button_mas[index_row].append(label)

            button_delete = tk.Button(scrollable_frame, text="Удалить запись",
                               command=lambda p1=Client.header[0], p2=Client.content[index_row][0]:
                               Client.sql_delete(p1, p2, scrollable_frame, root))
            button_delete.grid(row=index_row + 2, column=len(Client.header), sticky='nsew')
            Client.button_mas[index_row].append(button_delete)

        button = tk.Button(scrollable_frame, text="Добавить запись", font=("Arial", 16),
                           command=lambda: Client.add_new_row(root, scrollable_frame))
        button.grid(row=len(Client.content) + 2, column=0, columnspan=len_title, sticky='ew', padx=10,
                    pady=25)