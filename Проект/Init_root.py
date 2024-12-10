from tkinter import ttk

from db_connection import DbConnection
import tkinter as tk
from Author import Author
from Book import Book
from Client import Client
from Order import Order
from User import User


class InitRoot:

    @staticmethod
    def initial(login_frame, p1, p2):
        login_param = p1.get()
        password_param = p2.get()
        query = 'SELECT * FROM Пользователи WHERE Идентификатор = ? AND Пароль = ?'
        DbConnection.cursor.execute(query, (login_param, password_param))
        user = DbConnection.cursor.fetchall()

        if len(user) == 0:
            return
        else:
            print(user)
            User.current_id = user[0][0]
            User.current_status = user[0][6]

        login_frame.destroy()

        def configure_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        root = tk.Tk()
        root.title("База данных магазина")
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

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind("<Configure>", configure_scrollregion)

        label_user = tk.Label(mainFrame, text=f"User: {User.current_id}", fg="black", bg="#D3D3D3", font=("Arial", 14))
        label_user.pack(anchor='w', padx=10, pady=5)

        label_status = tk.Label(mainFrame, text=f"Привилегии: {User.current_status}", fg="black", bg="#D3D3D3", font=("Arial", 14))
        label_status.pack(anchor='w', padx=10)

        tables_title = tk.Label(mainFrame, text="База данных", fg="black", bg="#D3D3D3",
                                font=("Impact", 25, "underline"))
        tables_title.pack(anchor='w', padx=10, pady=25)

        author_table = tk.Label(mainFrame, text="Авторы", fg="black", bg="#D3D3D3", cursor="hand2", font=("Arial", 18))
        author_table.pack(anchor='w', padx=10, pady=5)
        author_table.bind("<Button-1>", lambda e: Author.show_data(scrollable_frame, root))

        line_frame = tk.Frame(mainFrame, height=2, bg="black")
        line_frame.pack(fill=tk.X)

        author_table = tk.Label(mainFrame, text="Книги", fg="black", bg="#D3D3D3", cursor="hand2", font=("Arial", 18))
        author_table.pack(anchor='w', padx=10, pady=5)
        author_table.bind("<Button-1>", lambda e: Book.show_data(scrollable_frame, root))

        line_frame = tk.Frame(mainFrame, height=2, bg="black")
        line_frame.pack(fill=tk.X)

        author_table = tk.Label(mainFrame, text="Клиенты", fg="black", bg="#D3D3D3", cursor="hand2", font=("Arial", 18))
        author_table.pack(anchor='w', padx=10, pady=5)
        author_table.bind("<Button-1>", lambda e: Client.show_data(scrollable_frame, root))

        line_frame = tk.Frame(mainFrame, height=2, bg="black")
        line_frame.pack(fill=tk.X)

        author_table = tk.Label(mainFrame, text="Заказы", fg="black", bg="#D3D3D3", cursor="hand2", font=("Arial", 18))
        author_table.pack(anchor='w', padx=10, pady=5)
        author_table.bind("<Button-1>", lambda e: Order.show_data(scrollable_frame))

        line_frame = tk.Frame(mainFrame, height=2, bg="black")
        line_frame.pack(fill=tk.X)

        if User.current_status == "1":
            author_table = tk.Label(mainFrame, text="Пользователи", fg="black", bg="#D3D3D3", cursor="hand2", font=("Arial", 18))
            author_table.pack(anchor='w', padx=10, pady=5)
            author_table.bind("<Button-1>", lambda e: User.show_data(scrollable_frame, root))

            line_frame = tk.Frame(mainFrame, height=2, bg="black")
            line_frame.pack(fill=tk.X)



        root.mainloop()