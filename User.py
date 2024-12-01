import tkinter as tk
from tkinter import messagebox, ttk
from db_connection import DbConnection


class User:
    header = ["Идентификатор", "Имя", "Фамилия", "Отчество", "Дата рождения"]
    content = []
    button_mas = []
    current_id = ""
    current_status = ""

    @staticmethod
    def get_data():
        User.content.clear()
        query = f"SELECT Идентификатор, Имя, Фамилия, Отчество, [Дата рождения] FROM Пользователи;"
        DbConnection.cursor.execute(query)
        User.content = DbConnection.cursor.fetchall()

    @staticmethod
    def sql_delete(header, value, scrollable_frame, root):
        query = f"DELETE FROM Пользователи WHERE [{header}] = ?"
        try:
            DbConnection.cursor.execute(query, (value,))
            #DbConnection.conn.commit()
            messagebox.showinfo("Информация", "Запись успешно удалена!")
            User.show_data(scrollable_frame, root)
        except Exception as e:
            messagebox.showwarning("Предупреждение", f"Непредвиденная ошибка: \n{e}\n\n")

    @staticmethod
    def validate(id, surname, name, last, birth, new_window, scrollable_frame, root):
        data = [id.get(), surname.get(), name.get(), last.get(), birth.get()]

        User.sql_add(data, new_window, scrollable_frame, root)

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

        label_id = ttk.Label(new_window, text="Идентификатор:", font=("Arial", 14))
        label_id.grid(row=0, column=0, sticky='nsew', pady=20)
        entry_id = ttk.Entry(new_window)
        entry_id.grid(row=0, column=1, sticky='nsew', pady=20, padx=10)


        label_name = ttk.Label(new_window, text="Имя:", font=("Arial", 14))
        label_name.grid(row=1, column=0, sticky='nsew', pady=20)
        entry_name = ttk.Entry(new_window)
        entry_name.grid(row=1, column=1, sticky='nsew', pady=20, padx=10)

        label_surname = ttk.Label(new_window, text="Фамилия:", font=("Arial", 14))
        label_surname.grid(row=2, column=0, sticky='nsew', pady=20)
        entry_surname = ttk.Entry(new_window)
        entry_surname.grid(row=2, column=1, sticky='nsew', pady=20, padx=10)

        label_last = ttk.Label(new_window, text="Отчество (н/о):", font=("Arial", 14))
        label_last.grid(row=3, column=0, sticky='nsew', pady=20)
        entry_last = ttk.Entry(new_window)
        entry_last.grid(row=3, column=1, sticky='nsew', pady=20, padx=10)

        label_birth = ttk.Label(new_window, text="birth:", font=("Arial", 14))
        label_birth.grid(row=4, column=0, sticky='nsew', pady=20)
        entry_birth = ttk.Entry(new_window)
        entry_birth.grid(row=4, column=1, sticky='nsew', pady=20, padx=10)


        button = ttk.Button(new_window, text="Добавить",
                            command=lambda: User.validate(entry_id, entry_surname, entry_name, entry_last, entry_birth, new_window, scrollable_frame, root))
        button.grid(row=len(User.header), column=0, columnspan=2, sticky='ew', padx=10, pady=25)


    @staticmethod
    def sql_add(data, new_window, scrollable_frame, root):
        try:
            query = f"INSERT INTO Пользователи (Идентификатор, Имя, Фамилия, Отчество, [Дата рождения]) VALUES (?, ?, ?, ?, ?)"
            DbConnection.cursor.execute(query, data)
            #DbConnection.conn.commit()
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
        new_window.title("Редактирование")

        label = ttk.Label(new_window, text=f"Новое значение '{change}': ", font=("Arial", 14))
        label.grid(row=0, column=0, sticky='nsew', pady=25, padx=10)
        entry = ttk.Entry(new_window)
        entry.grid(row=0, column=1, sticky='nsew', pady=25, padx=10)
        button = ttk.Button(new_window, text="Обновить",
                            command=lambda: User.sql_update(key, value, change, entry.get(), new_window, scrollable_frame, root))
        button.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=25)


    @staticmethod
    def sql_update(key, value, change, entry_value, new_window, scrollable_frame, root):
        query = f"UPDATE Пользователи " \
                f"SET [{change}] = ? " \
                f"WHERE [Идентификатор] = ? "

        try:
            DbConnection.cursor.execute(query, (entry_value, value))
            #DbConnection.conn.commit()
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



