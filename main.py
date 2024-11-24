import pyodbc
import sys
import os
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def connect_to_access_db(db_file: str):
    connection_string = rf'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_file};'
    return pyodbc.connect(connection_string)


def close_connection(conn: pyodbc.Connection):
    conn.close()


def get_all_tables(cursor):
    tables = []
    for table in cursor.tables(tableType='TABLE'):
        tables.append(table)

    return tables

def update_scrollregion():
    canvas.configure(scrollregion=canvas.bbox("all"))


def show_content(label_text):
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    print(f"Вы нажали на: {label_text}")
    query = f"SELECT * FROM [{label_text}];"
    cursor.execute(query)
    content = cursor.fetchall()
    header = [column[0] for column in cursor.description]

    len_title = len(header)
    title = tk.Label(scrollable_frame, text=label_text, fg="black", font=("Impact", 20))
    title.grid(row=0, column=0, columnspan=len_title, sticky='ew', padx=10, pady=25)

    for index_column, element in enumerate(header, start=0):
        label = tk.Label(scrollable_frame, text=element, fg="black", font=("Arial", 16, "bold"))
        label.grid(row=1, column=index_column, sticky='nsew', padx=10)

    for index_row, rows in enumerate(content, start=0):
        value = content[index_row][0]
        for index_column, element in enumerate(rows, start=0):
            label = tk.Label(scrollable_frame, text=element, fg="black", cursor="hand2", font=("Arial", 14))
            label.grid(row=index_row + 2, column=index_column, sticky='nsew')
            label.bind("<Button-1>", lambda e, p1 = label_text, p2 = header[0], p3 = value, p4 = header[index_column]: update(p1, p2, p3, p4))
        button = tk.Button(scrollable_frame, text="Удалить запись", command=lambda: sql_delete(label_text, header[0], value))
        button.grid(row=index_row + 2, column=len(header), sticky='nsew')

    button = tk.Button(scrollable_frame, text="Добавить запись", font=("Arial", 16), command=lambda: add_row(label_text, header))
    button.grid(row=len(content) + 2, column=0, columnspan=len_title, sticky='ew', padx=10, pady=25)  # Размещаем кнопку с отступом

def update(title, key, value, change):
    query = f"UPDATE [{title}] "\
            f"SET [{change}] = ? "\
            f"WHERE [{key}] = ? "

    new_window = tk.Toplevel(root)
    new_window.title("Редактирование")

    label = ttk.Label(new_window, text=f"Новое значение '{change}': ", font=("Arial", 14))
    label.grid(row=0, column=0, sticky='nsew', pady=25, padx=10)
    entry = ttk.Entry(new_window)
    entry.grid(row=0, column=1, sticky='nsew', pady=25,padx=10)
    button = ttk.Button(new_window, text="Обновить", command=lambda: sql_update(query, entry.get(), value, title, new_window))
    button.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=25)

def sql_update(query, entry_value, value, title, new_window):
    print(query)
    print(entry_value)
    print(value)
    try:
        cursor.execute(query, (entry_value, value))
        new_window.destroy()
        messagebox.showinfo("Информация", "Запись успешно обновлена!")
        show_content(title)
    except Exception as e:
        messagebox.showwarning("Предупреждение", f"Непредвиденная ошибка: \n{e}\n\nПопробуйте ввести другие данные\n")
        new_window.lift()


def add_row(title, header):
    new_window = tk.Toplevel(root)
    new_window.title("Добавление")

    mas_entry = []
    for index, element in enumerate(header, start=0):
        label = ttk.Label(new_window, text=f"{element}: ", font=("Arial", 14))
        label.grid(row=index, column=0, sticky='nsew', pady=25)

        mas_entry.append(ttk.Entry(new_window))
        mas_entry[index].grid(row=index, column=1, sticky='nsew', pady=25, padx=10)


    button = ttk.Button(new_window, text="Добавить", command=lambda: sql_add(header, title, mas_entry, new_window))
    button.grid(row=len(header), column=0, columnspan=2, sticky='ew', padx=10, pady=25)

def sql_add(header, title, mas_entry, new_window):
    line_header = "("
    line = "("

    for i in header:
        line_header += f"[{i}], "
        line += "?, "

    line_header = line_header[:-2] + ")"
    line = line[:-2] + ")"

    mas = []
    for i in mas_entry:
        mas.append(i.get())
    try:
        query = f"INSERT INTO [{title}] {line_header} VALUES {line}"
        print(mas)
        print(query)
        print(mas_entry)

        cursor.execute(f"INSERT INTO [{title}] {line_header} VALUES {line}", mas)
        new_window.destroy()
        messagebox.showinfo("Информация", "Запись успешно добавлена!")
        show_content(title)
    except Exception as e:
        messagebox.showwarning("Предупреждение", f"Непредвиденная ошибка: \n{e}\n\nПопробуйте ввести другие данные\n")
        new_window.lift()

def sql_delete(text, header, rows):
    query = f"DELETE FROM [{text}] WHERE [{header}] = ?"
    try:
        cursor.execute(query, (rows,))
        messagebox.showinfo("Информация", "Запись успешно удалена!")
        show_content(text)
    except Exception as e:
        messagebox.showwarning("Предупреждение", f"Непредвиденная ошибка: \n{e}\n\n")


root = tk.Tk()
root.title("Приложуха для access")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry(f"{width}x{height}")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=50)
root.grid_rowconfigure(0, weight=1)

mainFrame = tk.Frame(root, bg="#D3D3D3")
mainFrame.grid(row=0, column=0, sticky='nsew')

canvas = tk.Canvas(root)
scrollable_frame = tk.Frame(canvas)

# Создаем вертикальный и горизонтальный скроллеры
v_scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
h_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)

# Настраиваем Canvas
canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

# Размещаем Canvas и скроллеры
v_scrollbar.grid(row=0, column=2, sticky='ns')
h_scrollbar.grid(row=1, column=1, sticky='ew')
canvas.grid(row=0, column=1, sticky='nsew')

# Добавляем фрейм в Canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Обновляем область прокрутки при изменении размера фрейма
def configure_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", configure_scrollregion)

try:
    conn = connect_to_access_db(r'C:\Users\Андрей\Desktop\Совместные проекты\Labs-5-semester\Базы данных\Андрей\Лабораторная работа 6\DB.accdb')
    print("Подключение к базе данных успешно!")
except pyodbc.Error as ex:
    print("Ошибка подключения к базе данных: ", ex)
    sys.exit()


cursor = conn.cursor()

tables = get_all_tables(cursor)
tables_list = []
tables_title = tk.Label(mainFrame, text="Таблицы в базе данных", fg="black", bg="#D3D3D3", font=("Impact", 25, "underline"))
tables_title.pack(anchor='w', padx=10, pady=25)
for element in tables:
    label1 = tk.Label(mainFrame, text=element[2], fg="black", bg="#D3D3D3", cursor="hand2", font=("Arial", 18))
    label1.pack(anchor='w', padx=10, pady=5)
    label1.bind("<Button-1>", lambda e, text=element[2]: show_content(text))

    line_frame = tk.Frame(mainFrame, height=2, bg="black")
    line_frame.pack(fill=tk.X)

root.mainloop()

close_connection(conn)

