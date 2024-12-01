import tkinter as tk
from tkinter import messagebox, ttk
from db_connection import DbConnection


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
    def sql_delete(header, value, scrollable_frame, root):
        query = f"DELETE FROM Заказы WHERE [{header}] = ?"
        try:
            DbConnection.cursor.execute(query, (value,))
            #DbConnection.conn.commit()
            messagebox.showinfo("Информация", "Запись успешно удалена!")
            Order.show_data(scrollable_frame, root)
        except Exception as e:
            messagebox.showwarning("Предупреждение", f"Непредвиденная ошибка: \n{e}\n\n")


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
    def update(key, value, change, root, scrollable_frame):
        new_window = tk.Toplevel(root)
        new_window.title("Редактирование")

        label = ttk.Label(new_window, text=f"Новое значение '{change}': ", font=("Arial", 14))
        label.grid(row=0, column=0, sticky='nsew', pady=25, padx=10)
        entry = ttk.Entry(new_window)
        entry.grid(row=0, column=1, sticky='nsew', pady=25, padx=10)
        button = ttk.Button(new_window, text="Обновить",
                            command=lambda: Order.sql_update(key, value, change, entry.get(), new_window, scrollable_frame, root))
        button.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=25)


    @staticmethod
    def sql_update(key, value, change, entry_value, new_window, scrollable_frame, root):
        query = f"UPDATE Заказы " \
                f"SET [{change}] = ? " \
                f"WHERE [Идентификатор] = ? "

        try:
            DbConnection.cursor.execute(query, (entry_value, value))
            #DbConnection.conn.commit()
            new_window.destroy()
            messagebox.showinfo("Информация", "Запись успешно обновлена!")
            Order.show_data(scrollable_frame, root)
        except Exception as e:
            messagebox.showwarning("Предупреждение",
                                   f"Непредвиденная ошибка: \n{e}\n\nПопробуйте ввести другие данные\n")
            new_window.lift()

    @staticmethod
    def show_data(scrollable_frame, root):

        Order.get_data()

        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        len_title = len(Order.header)
        title = tk.Label(scrollable_frame, text="Заказы", fg="black", font=("Impact", 20))
        title.grid(row=0, column=0, columnspan=len_title, sticky='ew', padx=10, pady=25)

        for index_column, element in enumerate(Order.header, start=0):
            label = tk.Label(scrollable_frame, text=element, fg="black", font=("Arial", 16, "bold"))
            label.grid(row=1, column=index_column, sticky='nsew', padx=10)


        for index_row, rows in enumerate(Order.content, start=0):
            Order.button_mas.append([])
            value = Order.content[index_row][0]
            for index_column, element in enumerate(rows, start=0):
                label = tk.Label(scrollable_frame, text=element, fg="black", cursor="hand2", font=("Arial", 14))
                label.grid(row=index_row + 2, column=index_column, sticky='nsew')
                label.bind("<Button-1>", lambda e, p1=Order.header[0], p2=value, p3=Order.header[index_column]: Order.update(p1, p2, p3, root, scrollable_frame))
                Order.button_mas[index_row].append(label)

            button_delete = tk.Button(scrollable_frame, text="Удалить запись",
                               command=lambda p1=Order.header[0], p2=Order.content[index_row][0]:
                               Order.sql_delete(p1, p2, scrollable_frame, root))
            button_delete.grid(row=index_row + 2, column=len(Order.header), sticky='nsew')
            Order.button_mas[index_row].append(button_delete)



