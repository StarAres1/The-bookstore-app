import tkinter as tk
from tkinter import messagebox, ttk

import Book
from db_connection import DbConnection
from Book import Book


class Author:
    header = ["Идентификатор", "Фамилия", "Имя", "Отчество", "Страна"]
    content = []
    button_mas = []

    @staticmethod
    def get_data():
        Author.content.clear()
        query = f"SELECT * FROM Авторы;"
        DbConnection.cursor.execute(query)
        Author.content = DbConnection.cursor.fetchall()

    @staticmethod
    def sql_delete(header, value, scrollable_frame, root):
        query = f"DELETE FROM Авторы WHERE [{header}] = ?"
        check = Author.validate_delete(value)
        if check != 0:
            messagebox.showwarning("Предупреждение", check)
            return
        try:
            DbConnection.cursor.execute(query, (value,))
            DbConnection.commit()
            messagebox.showinfo("Информация", "Запись успешно удалена!")
            Author.show_data(scrollable_frame, root)
        except Exception as e:
            messagebox.showwarning("Предупреждение", f"Непредвиденная ошибка: \n{e}\n\n")

    @staticmethod
    def validate(id, surname, name, last, country, new_window, scrollable_frame, root):
        data = [id.get(), surname.get(), name.get(), last.get(), country.get()]
        error_message = "Ошибочный ввод: "
        is_error = False
        if not Author.validate_id(data[0]):
            error_message = error_message + "\nИдентификатор должен быть целым положительным числом и не должен быть занят."
            is_error = True
        if not Author.validate_name(data[1]):
            error_message = error_message + "\nФамилия может содержать только буквы кириллицы, пробелы, дефисы, точки и апострофы."
            is_error = True
        if not Author.validate_name(data[2]):
            error_message = error_message + "\nИмя может содержать только буквы кириллицы, пробелы, дефисы, точки и апострофы."
            is_error = True
        if not Author.validate_name(data[3]):
            error_message = error_message + "\nОтчество может содержать только буквы кириллицы, пробелы, дефисы, точки и апострофы."
            is_error = True
        if not Author.validate_country(data[4]):
            error_message = error_message + "\nНазвание страны может содержать только буквы кириллицы, пробелы, дефисы, точки и апострофы."
            is_error = True
        if is_error:
            messagebox.showinfo("Ошибка ввода", message=error_message)
        else:
            Author.sql_add(data, new_window, scrollable_frame, root)

    @staticmethod
    def validate_name(name):
        alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        permitted_symbols = " -.'"
        for i in range(len(name)):
            if not (name[i] in alphabet or name[i] in alphabet.upper() or name[i] in permitted_symbols):
                return False
        return True

    @staticmethod
    def validate_id(id):
        try:
            id = int(id)
            query = f"SELECT * FROM Авторы WHERE Идентификатор = ?"
            DbConnection.cursor.execute(query, (id,))
            author = DbConnection.cursor.fetchall()
            if len(author) != 0:
                return False
            if id > 0:
                return True
            return False
        except:
            return False

    @staticmethod
    def validate_country(country):
        alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        permitted_symbols = " -.'"
        for i in range(len(country)):
            if not (country[i] in alphabet or country[i] in alphabet.upper() or country[i] in permitted_symbols):
                return False
        return True

    @staticmethod
    def validate_delete(value):
        Book.get_data()
        for row in Book.content:
            if row[2] == value:
                return "Вы не можете удалить автора пока в базе данных есть его книги!"
        return 0

    @staticmethod
    def add_new_row(root, scrollable_frame):
        new_window = tk.Toplevel(root)
        new_window.title("Добавление")

        label_id = ttk.Label(new_window, text="Идентификатор:", font=("Arial", 14))
        label_id.grid(row=0, column=0, sticky='nsew', pady=20)
        entry_id = ttk.Entry(new_window)
        entry_id.grid(row=0, column=1, sticky='nsew', pady=20, padx=10)

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

        label_county = ttk.Label(new_window, text="Страна:", font=("Arial", 14))
        label_county.grid(row=4, column=0, sticky='nsew', pady=20)
        entry_county = ttk.Entry(new_window)
        entry_county.grid(row=4, column=1, sticky='nsew', pady=20, padx=10)


        button = ttk.Button(new_window, text="Добавить",
                            command=lambda: Author.validate(entry_id, entry_surname, entry_name, entry_last, entry_county, new_window, scrollable_frame, root))
        button.grid(row=len(Author.header), column=0, columnspan=2, sticky='ew', padx=10, pady=25)


    @staticmethod
    def sql_add(data, new_window, scrollable_frame, root):
        try:
            query = f"INSERT INTO Авторы (Идентификатор, Фамилия, Имя, Отчество, Страна) VALUES (?, ?, ?, ?, ?)"
            DbConnection.cursor.execute(query, data)
            DbConnection.commit()
            new_window.destroy()
            messagebox.showinfo("Информация", "Запись успешно добавлена!")
            Author.show_data(scrollable_frame, root)
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
                            command=lambda: Author.sql_update(value, change, entry.get(), new_window, scrollable_frame, root))
        button.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=25)


    @staticmethod
    def sql_update(value, change, entry_value, new_window, scrollable_frame, root):
        query = f"UPDATE Авторы " \
                f"SET [{change}] = ? " \
                f"WHERE [Идентификатор] = ? "
        if change == 'Идентификатор':
            if not Author.validate_id(entry_value):
                messagebox.showinfo("Ошибка ввода",
                                    message="Идентификатор должен быть целым положительным числом и не должен быть занят.")
                return False
        elif change == 'Имя':
            if not Author.validate_name(entry_value):
                messagebox.showinfo("Ошибка ввода",
                                    message="Имя может содержать только буквы кириллицы, пробелы, дефисы, точки и апострофы.")
                return False
        elif change == 'Фамиля':
            if not Author.validate_name(entry_value):
                messagebox.showinfo("Ошибка ввода",
                                    message="Фамилия может содержать только буквы кириллицы, пробелы, дефисы, точки и апострофы.")
                return False
        elif change == 'Отчество':
            if not Author.validate_name(entry_value):
                messagebox.showinfo("Ошибка ввода",
                                    message="Отчество может содержать только буквы кириллицы, пробелы, дефисы, точки и апострофы.")
                return False
        elif change == 'Страна':
            if not Author.validate_country(entry_value):
                messagebox.showinfo("Ошибка ввода",
                                    message="Название страны может содержать только буквы кириллицы, пробелы, дефисы, точки и апострофы.")
                return False
        try:
            DbConnection.cursor.execute(query, (entry_value, value))
            DbConnection.commit()
            new_window.destroy()
            messagebox.showinfo("Информация", "Запись успешно обновлена!")
            Author.show_data(scrollable_frame, root)
        except Exception as e:
            messagebox.showwarning("Предупреждение",
                                   f"Непредвиденная ошибка: \n{e}\n\nПопробуйте ввести другие данные\n")
            new_window.lift()

    @staticmethod
    def show_data(scrollable_frame, root):

        Author.get_data()

        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        len_title = len(Author.header)
        title = tk.Label(scrollable_frame, text="Авторы", fg="black", font=("Impact", 20))
        title.grid(row=0, column=0, columnspan=len_title, sticky='ew', padx=10, pady=25)

        for index_column, element in enumerate(Author.header, start=0):
            label = tk.Label(scrollable_frame, text=element, fg="black", font=("Arial", 16, "bold"))
            label.grid(row=1, column=index_column, sticky='nsew', padx=10)


        for index_row, rows in enumerate(Author.content, start=0):
            Author.button_mas.append([])
            value = Author.content[index_row][0]
            for index_column, element in enumerate(rows, start=0):
                label = tk.Label(scrollable_frame, text=element, fg="black", cursor="hand2", font=("Arial", 14))
                label.grid(row=index_row + 2, column=index_column, sticky='nsew')
                label.bind("<Button-1>", lambda e, p1=Author.header[0], p2=value, p3=Author.header[index_column]: Author.update(p1, p2, p3, root, scrollable_frame))
                Author.button_mas[index_row].append(label)

            button_delete = tk.Button(scrollable_frame, text="Удалить запись",
                               command=lambda p1=Author.header[0], p2=Author.content[index_row][0]:
                               Author.sql_delete(p1, p2, scrollable_frame, root))
            button_delete.grid(row=index_row + 2, column=len(Author.header), sticky='nsew')
            Author.button_mas[index_row].append(button_delete)

        button = tk.Button(scrollable_frame, text="Добавить запись", font=("Arial", 16),
                           command=lambda: Author.add_new_row(root, scrollable_frame))
        button.grid(row=len(Author.content) + 2, column=0, columnspan=len_title, sticky='ew', padx=10,
                    pady=25)