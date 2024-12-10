import tkinter as tk
from tkinter import messagebox, ttk
from db_connection import DbConnection
import datetime


class User:
    header = ["Идентификатор", "Фамилия", "Имя", "Отчество", "Дата рождения", "Уровень привелегий"]
    content = []
    button_mas = []
    current_id = ""
    current_status = ""

    @staticmethod
    def get_data():
        User.content.clear()
        query = f"SELECT Идентификатор, Фамилия, Имя, Отчество, [Дата рождения], [Уровень привелегий] FROM Пользователи;"
        DbConnection.cursor.execute(query)
        User.content = DbConnection.cursor.fetchall()

    @staticmethod
    def sql_delete(header, value, scrollable_frame, root):
        query = f"DELETE FROM Пользователи WHERE [{header}] = ?"
        try:
            DbConnection.cursor.execute(query, (value,))
            DbConnection.commit()
            messagebox.showinfo("Информация", "Запись успешно удалена!")
            User.show_data(scrollable_frame, root)
        except Exception as e:
            messagebox.showwarning("Предупреждение", f"Непредвиденная ошибка: \n{e}\n\n")


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
    def validate_status(status):
        if status == '1' or status == '2':
            return True
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
    def validate(surname, name, last, birth, password, status, new_window, scrollable_frame, root):
        error_message = "Ошибочный ввод: "
        is_error = False
        data = [surname.get(), name.get(), last.get(), birth.get(), password.get(), status.get()]
        if not User.validate_name(data[0]):
            is_error = True
            error_message = error_message + "\nФамилия может содержать только буквы кириллицы, пробелы, дефисы, точки и апострофы"
        if not User.validate_name(data[1]):
            is_error = True
            error_message = error_message + "\nИмя может содержать только буквы кириллицы, пробелы, дефисы, точки и апострофы"
        if data[2]:
            if not User.validate_name(data[2]):
                is_error = True
                error_message = error_message + "\nОтчество может содержать только буквы кириллицы, пробелы, дефисы, точки и апострофы"
        if not User.validate_date(data[3]):
            is_error = True
            error_message = error_message + "\nДата может быть только в формате ГГГГ-ММ-ДД и должна быть раньше сегодняшнего дня"
        if not User.validate_status(data[5]):
            is_error = True
            error_message = error_message + "\nУровень равен 1, если пользователь является менеджером, и 2 - если обычным сотрудником"
        if is_error:
            messagebox.showinfo("Ошибка ввода", message=error_message)
        else:
            User.sql_add(data, new_window, scrollable_frame, root)

    @staticmethod
    def add_new_row(root, scrollable_frame):
        new_window = tk.Toplevel(root)
        new_window.attributes('-topmost', True)
        new_window.title("Добавление")

        label_surname = ttk.Label(new_window, text="Фамилия:", font=("Arial", 14))
        label_surname.grid(row=1, column=0, sticky='nsew', pady=20)
        entry_surname = ttk.Entry(new_window)
        entry_surname.grid(row=1, column=1, sticky='nsew', pady=20, padx=10)

        label_name = ttk.Label(new_window, text="Имя:", font=("Arial", 14))
        label_name.grid(row=2, column=0, sticky='nsew', pady=20)
        entry_name = ttk.Entry(new_window)
        entry_name.grid(row=2, column=1, sticky='nsew', pady=20, padx=10)

        label_last = ttk.Label(new_window, text="Отчество (н/о):", font=("Arial", 14))
        label_last.grid(row=3, column=0, sticky='nsew', pady=20)
        entry_last = ttk.Entry(new_window)
        entry_last.grid(row=3, column=1, sticky='nsew', pady=20, padx=10)

        label_birth = ttk.Label(new_window, text="Дата рождения (ГГГГ-ММ-ДД)", font=("Arial", 14))
        label_birth.grid(row=4, column=0, sticky='nsew', pady=20)
        entry_birth = ttk.Entry(new_window)
        entry_birth.grid(row=4, column=1, sticky='nsew', pady=20, padx=10)

        label_pass = ttk.Label(new_window, text="Пароль: ", font=("Arial", 14))
        label_pass.grid(row=5, column=0, sticky='nsew', pady=20)
        entry_pass = ttk.Entry(new_window)
        entry_pass.grid(row=5, column=1, sticky='nsew', pady=20, padx=10)

        label_status = ttk.Label(new_window, text="Уровень(1/2): ", font=("Arial", 14))
        label_status.grid(row=6, column=0, sticky='nsew', pady=20)
        entry_status = ttk.Entry(new_window)
        entry_status.grid(row=6, column=1, sticky='nsew', pady=20, padx=10)


        button = ttk.Button(new_window, text="Добавить",
                            command=lambda: User.validate(entry_surname, entry_name, entry_last, entry_birth, entry_pass, entry_status, new_window, scrollable_frame, root))
        button.grid(row=len(User.header)+1, column=0, columnspan=2, sticky='ew', padx=10, pady=25)


    @staticmethod
    def sql_add(data, new_window, scrollable_frame, root):
        try:
            query = f"INSERT INTO Пользователи (Фамилия, Имя, Отчество, [Дата рождения], Пароль, [Уровень привелегий]) VALUES (?, ?, ?, ?, ?, ?)"
            DbConnection.cursor.execute(query, data)
            DbConnection.commit()
            new_window.destroy()
            messagebox.showinfo("Информация", "Запись успешно добавлена!")
            User.show_data(scrollable_frame, root)
        except Exception as e:
            messagebox.showwarning("Предупреждение",
                                       f"Непредвиденная ошибка: \n{e}\n\nПопробуйте ввести другие данные\n")
            new_window.lift()

    @staticmethod
    def update(key, value, change, root, scrollable_frame):
        new_window = tk.Toplevel(root)
        new_window.attributes("-topmost", True)
        new_window.title("Редактирование")

        label = ttk.Label(new_window, text=f"Новое значение '{change}': ", font=("Arial", 14))
        label.grid(row=0, column=0, sticky='nsew', pady=25, padx=10)
        entry = ttk.Entry(new_window)
        entry.grid(row=0, column=1, sticky='nsew', pady=25, padx=10)
        button = ttk.Button(new_window, text="Обновить",
                            command=lambda: User.sql_update(value, change, entry.get(), new_window, scrollable_frame, root))
        button.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=25)


    @staticmethod
    def sql_update(value, change, entry_value, new_window, scrollable_frame, root):
        query = f"UPDATE Пользователи " \
                f"SET [{change}] = ? " \
                f"WHERE [Идентификатор] = ? "
        if change == 'Идентификатор':
            if not User.validate_id(entry_value):
                messagebox.showinfo("Ошибка ввода",
                            message="Идентификатор должен быть целым положительным числом")
                return False
        elif change == 'Имя':
            if not User.validate_name(entry_value):
                messagebox.showinfo("Ошибка ввода",
                            message="Имя может содержать только буквы кириллицы, пробелы, дефисы, точки и апострофы")
                return False
        elif change == 'Фамилия':
            if not User.validate_name(entry_value):
                messagebox.showinfo("Ошибка ввода",
                            message="Фамилия может содержать только буквы кириллицы, пробелы, дефисы, точки и апострофы")
                return False
        elif change == 'Отчество':
            if not User.validate_name(entry_value):
                messagebox.showinfo("Ошибка ввода",
                            message="Отчество может содержать только буквы кириллицы, пробелы, дефисы, точки и апострофы")
                return False
        elif change == 'Дата рождения':
            if not User.validate_date(entry_value):
                messagebox.showinfo("Ошибка ввода",
                            message="Дата может быть только в формате ГГГГ-ММ-ДД и должна быть раньше сегодняшнего дня")
                return False
        elif change == 'Уровень привелегий':
            if not User.validate_status(entry_value):
                messagebox.showinfo("Ошибка ввода",
                            message="Уровень равен 1, если пользователь является менеджером, и 2 - если обычным сотрудником")
                return False

        try:
            print(change)
            DbConnection.cursor.execute(query, (entry_value, value))
            DbConnection.commit()
            new_window.destroy()
            messagebox.showinfo("Информация", "Запись успешно обновлена!")
            User.show_data(scrollable_frame, root)
        except Exception as e:
            messagebox.showwarning("Предупреждение",
                                   f"Непредвиденная ошибка: \n{e}\n\nПопробуйте ввести другие данные\n")
            new_window.lift()

    @staticmethod
    def show_data(scrollable_frame, root):

        User.get_data()

        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        len_title = len(User.header)
        title = tk.Label(scrollable_frame, text="Пользователи", fg="black", font=("Impact", 20))
        title.grid(row=0, column=0, columnspan=len_title, sticky='ew', padx=10, pady=25)

        for index_column, element in enumerate(User.header, start=0):
            label = tk.Label(scrollable_frame, text=element, fg="black", font=("Arial", 16, "bold"))
            label.grid(row=1, column=index_column, sticky='nsew', padx=10)


        for index_row, rows in enumerate(User.content, start=0):
            User.button_mas.append([])
            value = User.content[index_row][0]
            for index_column, element in enumerate(rows, start=0):
                label = tk.Label(scrollable_frame, text=element, fg="black", cursor="hand2", font=("Arial", 14))
                label.grid(row=index_row + 2, column=index_column, sticky='nsew')
                label.bind("<Button-1>", lambda e, p1=User.header[0], p2=value, p3=User.header[index_column]: User.update(p1, p2, p3, root, scrollable_frame))
                User.button_mas[index_row].append(label)

            button_delete = tk.Button(scrollable_frame, text="Удалить запись",
                               command=lambda p1=User.header[0], p2=User.content[index_row][0]:
                               User.sql_delete(p1, p2, scrollable_frame, root))
            button_delete.grid(row=index_row + 2, column=len(User.header), sticky='nsew')
            User.button_mas[index_row].append(button_delete)

        button = tk.Button(scrollable_frame, text="Добавить запись", font=("Arial", 16),
                           command=lambda: User.add_new_row(root, scrollable_frame))
        button.grid(row=len(User.content) + 2, column=0, columnspan=len_title, sticky='ew', padx=10,
                    pady=25)