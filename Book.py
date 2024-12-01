import tkinter as tk
from tkinter import messagebox, ttk
from db_connection import DbConnection


class Book:
    header = ["ISBN", "Название", "ID автора", "Издательство", "Год издания", "Количество", "Жанр", "Стоимость", "Тип обложки", "Страна издания"]
    content = []
    button_mas = []

    @staticmethod
    def get_data():
        Book.content.clear()
        query = f"SELECT * FROM Книги;"
        DbConnection.cursor.execute(query)
        Book.content = DbConnection.cursor.fetchall()

    @staticmethod
    def sql_delete(header, value, scrollable_frame, root):
        query = f"DELETE FROM Книги WHERE [{header}] = ?"
        try:
            DbConnection.cursor.execute(query, (value,))
            # DbConnection.conn.commit()
            messagebox.showinfo("Информация", "Запись успешно удалена!")
            Book.show_data(scrollable_frame, root)
        except Exception as e:
            messagebox.showwarning("Предупреждение", f"Непредвиденная ошибка: \n{e}\n\n")

    @staticmethod
    def validate(isbn, title, author, publisher, year, count, genre, amount, type, country,
                 new_window, scrollable_frame, root):
        data = [isbn.get(), title.get(), author.get(), publisher.get(), year.get(), count.get(), genre.get(),
                amount.get(), type.get(), country.get()]

        Book.sql_add(data, new_window, scrollable_frame, root)

    @staticmethod
    def validate_custom():
        pass

    @staticmethod
    def validate_update():
        pass

    @staticmethod
    def validate_delete():
        pass

    @staticmethod
    def add_new_row(root, scrollable_frame):
        new_window = tk.Toplevel(root)
        new_window.title("Добавление")

        label_isbn = ttk.Label(new_window, text="ISBN:", font=("Arial", 14))
        label_isbn.grid(row=0, column=0, sticky='nsew', pady=20)
        entry_isbn = ttk.Entry(new_window)
        entry_isbn.grid(row=0, column=1, sticky='nsew', pady=20, padx=10)

        label_title = ttk.Label(new_window, text="Название:", font=("Arial", 14))
        label_title.grid(row=1, column=0, sticky='nsew', pady=20)
        entry_title = ttk.Entry(new_window)
        entry_title.grid(row=1, column=1, sticky='nsew', pady=20, padx=10)

        label_author = ttk.Label(new_window, text="ID автора:", font=("Arial", 14))
        label_author.grid(row=2, column=0, sticky='nsew', pady=20)
        entry_author = ttk.Entry(new_window)
        entry_author.grid(row=2, column=1, sticky='nsew', pady=20, padx=10)

        label_publisher = ttk.Label(new_window, text="Издательство:", font=("Arial", 14))
        label_publisher.grid(row=3, column=0, sticky='nsew', pady=20)
        entry_publisher = ttk.Entry(new_window)
        entry_publisher.grid(row=3, column=1, sticky='nsew', pady=20, padx=10)

        label_year = ttk.Label(new_window, text="Год издания:", font=("Arial", 14))
        label_year.grid(row=4, column=0, sticky='nsew', pady=20)
        entry_year = ttk.Entry(new_window)
        entry_year.grid(row=4, column=1, sticky='nsew', pady=20, padx=10)

        label_count = ttk.Label(new_window, text="Количество:", font=("Arial", 14))
        label_count.grid(row=5, column=0, sticky='nsew', pady=20)
        entry_count = ttk.Entry(new_window)
        entry_count.grid(row=5, column=1, sticky='nsew', pady=20, padx=10)

        label_genre = ttk.Label(new_window, text="Жанр:", font=("Arial", 14))
        label_genre.grid(row=6, column=0, sticky='nsew', pady=20)
        entry_genre = ttk.Entry(new_window)
        entry_genre.grid(row=6, column=1, sticky='nsew', pady=20, padx=10)

        label_amount = ttk.Label(new_window, text="Стоимость:", font=("Arial", 14))
        label_amount.grid(row=7, column=0, sticky='nsew', pady=20)
        entry_amount = ttk.Entry(new_window)
        entry_amount.grid(row=7, column=1, sticky='nsew', pady=20, padx=10)

        label_type = ttk.Label(new_window, text="Тип обложки:", font=("Arial", 14))
        label_type.grid(row=8, column=0, sticky='nsew', pady=20)
        entry_type = ttk.Entry(new_window)
        entry_type.grid(row=8, column=1, sticky='nsew', pady=20, padx=10)

        label_country = ttk.Label(new_window, text="Страна издания:", font=("Arial", 14))
        label_country.grid(row=9, column=0, sticky='nsew', pady=20)
        entry_country = ttk.Entry(new_window)
        entry_country.grid(row=9, column=1, sticky='nsew', pady=20, padx=10)

        button = ttk.Button(new_window, text="Добавить",
                            command=lambda: Book.validate(entry_isbn, entry_title, entry_author, entry_publisher,
                                                            entry_year, entry_count, entry_genre, entry_amount, entry_type,
                                                            entry_country, new_window, scrollable_frame, root))
        button.grid(row=len(Book.header), column=0, columnspan=2, sticky='ew', padx=10, pady=25)

    @staticmethod
    def sql_add(data, new_window, scrollable_frame, root):
        try:
            query = (f"INSERT INTO Книги (ISBN, Название, [ID автора], Издательство, [Год издания], Количество, Жанр,"
                     f"Стоимость, [Тип обложки], [Страна издания]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
            DbConnection.cursor.execute(query, data)
            # DbConnection.conn.commit()
            new_window.destroy()
            messagebox.showinfo("Информация", "Запись успешно добавлена!")
            Book.show_data(scrollable_frame, root)
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
                            command=lambda: Book.sql_update(key, value, change, entry.get(), new_window,
                                                              scrollable_frame, root))
        button.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=25)

    @staticmethod
    def sql_update(key, value, change, entry_value, new_window, scrollable_frame, root):
        query = f"UPDATE Книги " \
                f"SET [{change}] = ? " \
                f"WHERE [ISBN] = ? "

        try:
            DbConnection.cursor.execute(query, (entry_value, value))
            # DbConnection.conn.commit()
            new_window.destroy()
            messagebox.showinfo("Информация", "Запись успешно обновлена!")
            Book.show_data(scrollable_frame, root)
        except Exception as e:
            messagebox.showwarning("Предупреждение",
                                   f"Непредвиденная ошибка: \n{e}\n\nПопробуйте ввести другие данные\n")
            new_window.lift()

    @staticmethod
    def show_data(scrollable_frame, root):

        Book.get_data()

        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        len_title = len(Book.header)
        title = tk.Label(scrollable_frame, text="Книги", fg="black", font=("Impact", 20))
        title.grid(row=0, column=0, columnspan=len_title, sticky='ew', padx=10, pady=25)

        for index_column, element in enumerate(Book.header, start=0):
            label = tk.Label(scrollable_frame, text=element, fg="black", font=("Arial", 16, "bold"))
            label.grid(row=1, column=index_column, sticky='nsew', padx=10)

        for index_row, rows in enumerate(Book.content, start=0):
            Book.button_mas.append([])
            value = Book.content[index_row][0]
            for index_column, element in enumerate(rows, start=0):
                label = tk.Label(scrollable_frame, text=element, fg="black", cursor="hand2", font=("Arial", 14))
                label.grid(row=index_row + 2, column=index_column, sticky='nsew')
                label.bind("<Button-1>",
                           lambda e, p1=Book.header[0], p2=value, p3=Book.header[index_column]: Book.update(p1,
                                                                                                                  p2,
                                                                                                                  p3,
                                                                                                                  root,
                                                                                                                  scrollable_frame))
                Book.button_mas[index_row].append(label)

            button_delete = tk.Button(scrollable_frame, text="Удалить запись",
                                      command=lambda p1=Book.header[0], p2=Book.content[index_row][0]:
                                      Book.sql_delete(p1, p2, scrollable_frame, root))
            button_delete.grid(row=index_row + 2, column=len(Book.header), sticky='nsew')
            Book.button_mas[index_row].append(button_delete)

        button = tk.Button(scrollable_frame, text="Добавить запись", font=("Arial", 16),
                           command=lambda: Book.add_new_row(root, scrollable_frame))
        button.grid(row=len(Book.content) + 2, column=0, columnspan=len_title, sticky='ew', padx=10,
                    pady=25)



