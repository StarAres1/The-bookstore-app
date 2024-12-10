import unittest
from Book import Book
from db_connection import DbConnection
import tkinter as tk
from tkinter import ttk
from unittest.mock import patch
import  datetime


class TestClient(unittest.TestCase):
    def setUp(self):
        DbConnection.connect_to_access_db(r'C:\Users\User\PycharmProjects\BookStoreByTI\DB.accdb')

    def test_get_data(self):
        Book.get_data()
        self.assertEqual(100, Book.content[1][0])
        self.assertEqual('Око мира', Book.content[1][1])
        self.assertEqual(3, Book.content[1][2])
        self.assertEqual('Махаон', Book.content[1][3])
        self.assertEqual(2010, Book.content[1][4])
        self.assertEqual(100, Book.content[1][5])
        self.assertEqual('Эпическое фэнтези', Book.content[1][6])
        self.assertEqual('2050.0', str(float(Book.content[1][7])))
        self.assertEqual('Твердая', Book.content[1][8])
        self.assertEqual('Россия', Book.content[1][9])

    def test_sql_delete_positive(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            Book.get_data()
            number1 = len(Book.content)
            Book.sql_delete('ISBN', 100, scrollable_frame, root)
            number2 = len(Book.content)
            self.assertEqual(number2, number1 - 1)

    def test_sgl_delete_negative(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            Book.get_data()
            number1 = len(Book.content)
            try:
                Book.sql_delete('Идентификатор', 3, scrollable_frame, root)
            except:
                pass
            number2 = len(Book.content)
            self.assertEqual(number2, number1)

    def test_validate_isbn_positive(self):
        self.assertEqual(True, Book.validate_isbn('122'))

    def test_validate_isbn_negative(self):
        self.assertEqual(False, Book.validate_isbn('556++'))

    def test_validate_author_positive(self):
        self.assertEqual(True, Book.validate_author('2'))

    def test_validate_author_negative(self):
        self.assertEqual(False, Book.validate_author('8'))

    def test_validate_year_positive(self):
        self.assertEqual(True, Book.validate_year('2000'))

    def test_validate_year_negative(self):
        self.assertEqual(False, Book.validate_year('8888'))

    def test_validate_amount_positive(self):
        self.assertEqual(True, Book.validate_amount('2'))

    def test_validate_amount_negative(self):
        self.assertEqual(False, Book.validate_amount('-9'))

    def test_validate_genre_positive(self):
        self.assertEqual(True, Book.validate_genre('Классика'))

    def test_validate_genre_negative(self):
        self.assertEqual(False, Book.validate_genre('8'))

    def test_validate_count_positive(self):
        self.assertEqual(True, Book.validate_count('100'))

    def test_validate_count_negative(self):
        self.assertEqual(False, Book.validate_count('-8'))

    def test_validate_type_positive(self):
        self.assertEqual(True, Book.validate_genre('Мягкая'))

    def test_validate_type_negative(self):
        self.assertEqual(False, Book.validate_genre('888'))

    def test_validate_country_positive(self):
        self.assertEqual(True, Book.validate_genre('Кукуево'))

    def test_validate_country_negative(self):
        self.assertEqual(False, Book.validate_genre('8'))

    def test_validate_positive(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            isbn = ttk.Entry(new_window)
            title = ttk.Entry(new_window)
            author = ttk.Entry(new_window)
            publisher = ttk.Entry(new_window)
            year = ttk.Entry(new_window)
            count = ttk.Entry(new_window)
            genre = ttk.Entry(new_window)
            amount = ttk.Entry(new_window)
            ctype = ttk.Entry(new_window)
            country = ttk.Entry(new_window)

            isbn.insert(0, '55')
            title.insert(0, 'Хаха')
            author.insert(0, '4')
            publisher.insert(0, 'Кукуево')
            year.insert(0, '2005')
            count.insert(0, '666')
            genre.insert(0, 'Роман')
            amount.insert(0, '555')
            ctype.insert(0, 'Мягкая')
            country.insert(0, 'Кукуево')
            Book.get_data()
            number1 = len(Book.content)
            Book.validate(isbn,title,author,publisher,year,count,genre,amount,ctype,country,new_window, scrollable_frame,root)
            number2 = len(Book.content)
            self.assertEqual(number2, number1+1)

    def test_validate_negative(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            isbn = ttk.Entry(new_window)
            title = ttk.Entry(new_window)
            author = ttk.Entry(new_window)
            publisher = ttk.Entry(new_window)
            year = ttk.Entry(new_window)
            count = ttk.Entry(new_window)
            genre = ttk.Entry(new_window)
            amount = ttk.Entry(new_window)
            ctype = ttk.Entry(new_window)
            country = ttk.Entry(new_window)

            isbn.insert(0, '120')
            title.insert(0, 'Хаха')
            author.insert(0, '8')
            publisher.insert(0, 'Кукуево')
            year.insert(0, '20000')
            count.insert(0, '666')
            genre.insert(0, 'Роман55')
            amount.insert(0, '555jj')
            ctype.insert(0, 'Мягкая5')
            country.insert(0, 'Кукуево55')
            Book.get_data()
            number1 = len(Book.content)
            Book.validate(isbn,title,author,publisher,year,count,genre,amount,ctype,country,new_window, scrollable_frame,root)
            number2 = len(Book.content)
            self.assertEqual(number2, number1)

    def test_add(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            Book.add_new_row(root, scrollable_frame)
            widgets = root.winfo_children()[-1].winfo_children()
            self.assertEqual("Добавление", root.winfo_children()[-1].title())
            self.assertEqual("ISBN:", widgets[0].cget('text'))
            self.assertEqual("Название:", widgets[2].cget('text'))
            self.assertEqual("ID автора:", widgets[4].cget('text'))
            self.assertEqual("Издательство:", widgets[6].cget('text'))
            self.assertEqual("Год издания:", widgets[8].cget('text'))
            self.assertEqual("Количество:", widgets[10].cget('text'))
            self.assertEqual("Жанр:", widgets[12].cget('text'))
            self.assertEqual("Стоимость:", widgets[14].cget('text'))
            self.assertEqual("Тип обложки:", widgets[16].cget('text'))
            self.assertEqual("Страна издания:", widgets[18].cget('text'))
            self.assertTrue(isinstance(widgets[1], tk.Entry))
            self.assertTrue(isinstance(widgets[3], tk.Entry))
            self.assertTrue(isinstance(widgets[5], tk.Entry))
            self.assertTrue(isinstance(widgets[7], tk.Entry))
            self.assertTrue(isinstance(widgets[9], tk.Entry))
            self.assertTrue(isinstance(widgets[11], tk.Entry))
            self.assertTrue(isinstance(widgets[13], tk.Entry))
            self.assertTrue(isinstance(widgets[15], tk.Entry))
            self.assertTrue(isinstance(widgets[17], tk.Entry))
            self.assertTrue(isinstance(widgets[19], tk.Entry))
            self.assertTrue(isinstance(widgets[20], ttk.Button))
            self.assertEqual("Добавить", widgets[20].cget('text'))

    def test_sql_add_positive(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            Book.get_data()
            number1 = len(Book.content)
            data = ['140','Хаха','3','Кукуевы','2000','100','Кукуевизм','1000','Твердая','Кукуево']
            Book.sql_add(data,new_window,scrollable_frame,root)
            Book.get_data()
            number2 = len(Book.content)
            self.assertEqual(number2,number1+1)

    def test_sql_add_negative(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            Book.get_data()
            number1 = len(Book.content)
            data = ['120','Хаха1','38','Кукуевы','20000','100.h','Кукуевизм5','1000j','Твердая5','Кукуево5']
            Book.sql_add(data,new_window,scrollable_frame,root)
            Book.get_data()
            number2 = len(Book.content)
            self.assertEqual(number2,number1)

    def test_update(self):
        root = tk.Tk()
        canvas = tk.Canvas(root)
        scrollable_frame = tk.Frame(canvas)
        Book.update(4, 120, 'Название', root, scrollable_frame)
        widgets = root.winfo_children()[-1].winfo_children()
        self.assertEqual("Новое значение 'Название': ", widgets[0].cget('text'))
        self.assertEqual('Обновить', widgets[2].cget('text'))
        self.assertTrue(isinstance(widgets[1],tk.Entry))
        self.assertTrue(isinstance(widgets[2],ttk.Button))

    def test_sql_update_positive(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            shapka = ["ISBN", "Название", "ID автора", "Издательство", "Год издания", "Количество", "Жанр", "Стоимость", "Тип обложки", "Страна издания"]
            data = [40,'Привет',4,'Пока', 2000, 120, 'Всё опять', '1000', 'Твердая', 'Кувырком' ]
            Book.sql_update(120, shapka[1], data[1], new_window, scrollable_frame, root)
            Book.sql_update(120, shapka[2], data[2], new_window, scrollable_frame, root)
            Book.sql_update(120, shapka[3], data[3], new_window, scrollable_frame, root)
            Book.sql_update(120, shapka[4], data[5], new_window, scrollable_frame, root)
            Book.sql_update(120, shapka[5], data[5], new_window, scrollable_frame, root)
            Book.sql_update(120, shapka[6], data[6], new_window, scrollable_frame, root)
            Book.sql_update(120, shapka[7], data[7], new_window, scrollable_frame, root)
            Book.sql_update(120, shapka[8], data[8], new_window, scrollable_frame, root)
            Book.sql_update(120, shapka[9], data[9], new_window, scrollable_frame, root)
            Book.get_data()
            data1 = Book.content[2]
            self.assertEqual(data1[1],data[1])
            self.assertEqual(data1[2],data[2])
            self.assertEqual(data1[3],data[3])
            self.assertEqual(data1[8],data[8])
            self.assertEqual(data1[9],data[9])

