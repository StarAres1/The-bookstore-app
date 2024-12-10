import unittest
from Author import Author
from db_connection import DbConnection
import tkinter as tk
from tkinter import ttk
from unittest.mock import patch


class TestAuthor(unittest.TestCase):
    def setUp(self):
        DbConnection.connect_to_access_db(r'C:\Users\User\PycharmProjects\BookStoreByTI\DB.accdb')

    def test_get_data(self):
        Author.get_data()
        self.assertEqual(Author.content[0][0],2)
        self.assertEqual(Author.content[0][1], 'Сандерсон')
        self.assertEqual(Author.content[0][2], 'Брендон')
        self.assertEqual(Author.content[0][3], None)
        self.assertEqual(Author.content[0][4], 'США')

        self.assertEqual(Author.content[1][0], 1)
        self.assertEqual(Author.content[1][1], 'Пушкин')
        self.assertEqual(Author.content[1][2], 'Александр')
        self.assertEqual(Author.content[1][3], 'Сергеевич')
        self.assertEqual(Author.content[1][4], 'Россия')

        self.assertEqual(Author.content[2][0], 3)
        self.assertEqual(Author.content[2][1], 'Роберт')
        self.assertEqual(Author.content[2][2], 'Джордан')
        self.assertEqual(Author.content[2][3], '')
        self.assertEqual(Author.content[2][4], 'США')

        self.assertEqual(Author.content[3][0], 4)
        self.assertEqual(Author.content[3][1], 'Стругацкие')
        self.assertEqual(Author.content[3][2], 'Аркадий/Борис')
        self.assertEqual(Author.content[3][3], 'Натановичи')
        self.assertEqual(Author.content[3][4], 'СССР')

    def test_sql_delete_positive(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            Author.get_data()
            number1 = len(Author.content)
            Author.sql_delete('Идентификатор',4,scrollable_frame,root)
            number2 = len(Author.content)
            self.assertEqual(number2, number1-1)

    def test_sgl_delete_negative(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            Author.get_data()
            number1 = len(Author.content)
            try:
                Author.sql_delete('Идентификатор', 3, scrollable_frame, root)
            except: pass
            number2 = len(Author.content)
            self.assertEqual(number2, number1)

    def test_validate_positive(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            id = ttk.Entry(new_window)
            surname = ttk.Entry(new_window)
            name = ttk.Entry(new_window)
            last = ttk.Entry(new_window)
            country = ttk.Entry(new_window)
            id.insert(0, 5)
            surname.insert(0, 'Хихи')
            name.insert(0, 'Хаха')
            country.insert(0, 'Хахандия')
            Author.get_data()
            number1 = len(Author.content)
            Author.validate(id,surname,name,last,country, new_window, scrollable_frame,root)
            number2 = len(Author.content)
            self.assertEqual(number2, number1+1)

    def test_validate_negative(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            id = ttk.Entry(new_window)
            surname = ttk.Entry(new_window)
            name = ttk.Entry(new_window)
            last = ttk.Entry(new_window)
            country = ttk.Entry(new_window)
            id.insert(0, 'g')
            surname.insert(0, 'Хихи+-')
            name.insert(0, 'Хаха+-')
            last.insert(0, 'Хаха+-')
            country.insert(0, 'Хахандия++')
            Author.get_data()
            number1 = len(Author.content)
            Author.validate(id,surname,name,last,country, new_window, scrollable_frame,root)
            number2 = len(Author.content)
            self.assertEqual(number2, number1)

    def test_validate_name_positive(self):
        self.assertEqual(True, Author.validate_name('Кнопка-Шнопка'))

    def test_validate_name_negative(self):
        self.assertEqual(False, Author.validate_name('556++'))

    def test_validate_id_positive(self):
        self.assertEqual(True, Author.validate_id('5'))

    def test_validate_id_negative(self):
        self.assertEqual(False, Author.validate_id('556++'))

    def test_validate_id_exists(self):
        self.assertEqual(False, Author.validate_id(4))

    def test_validate_country_positive(self):
        self.assertEqual(True, Author.validate_country('Кнопка'))

    def test_validate_country_negative(self):
        self.assertEqual(False, Author.validate_country('556++'))

    def test_validate_delete_positive(self):
        self.assertEqual(0,Author.validate_delete(4))

    def test_validate_delete_negative(self):
        self.assertEqual("Вы не можете удалить автора пока в базе данных есть его книги!",Author.validate_delete(2))

    def test_add(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            Author.add_new_row(root, scrollable_frame)
            widgets = root.winfo_children()[-1].winfo_children()
            self.assertEqual("Добавление", root.winfo_children()[-1].title())
            self.assertEqual("Идентификатор:", widgets[0].cget('text'))
            self.assertEqual("Фамилия:", widgets[2].cget('text'))
            self.assertEqual("Имя:", widgets[4].cget('text'))
            self.assertEqual("Отчество (н/о):", widgets[6].cget('text'))
            self.assertEqual("Страна:", widgets[8].cget('text'))
            self.assertTrue(isinstance(widgets[1], tk.Entry))
            self.assertTrue(isinstance(widgets[3], tk.Entry))
            self.assertTrue(isinstance(widgets[5], tk.Entry))
            self.assertTrue(isinstance(widgets[7], tk.Entry))
            self.assertTrue(isinstance(widgets[9], tk.Entry))
            self.assertTrue(isinstance(widgets[10], ttk.Button))
            self.assertEqual("Добавить", widgets[10].cget('text'))

    def test_sql_add_positive(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            Author.get_data()
            number1 = len(Author.content)
            data = [5,'Кукуев','Куку','','Кукуево']
            Author.sql_add(data,new_window,scrollable_frame,root)
            Author.get_data()
            number2 = len(Author.content)
            self.assertEqual(number2,number1+1)

    def test_sql_add_negative(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            Author.get_data()
            number1 = len(Author.content)
            data = [3,'Кукуев','Куку','','Кукуево']
            Author.sql_add(data,new_window,scrollable_frame,root)
            Author.get_data()
            number2 = len(Author.content)
            self.assertEqual(number2,number1)

    def test_sql_update_positive(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            Author.get_data()
            Author.sql_update(2,'Идентификатор',8,new_window,scrollable_frame,root)
            Author.sql_update(8, 'Фамилия', 'Кукин', new_window, scrollable_frame, root)
            Author.sql_update(8, 'Имя', 'Куку', new_window, scrollable_frame, root)
            Author.sql_update(8, 'Отчество', 'Кукуевич', new_window, scrollable_frame, root)
            Author.sql_update(8, 'Страна', 'Кукуево', new_window, scrollable_frame, root)
            Author.get_data()
            data1 = Author.content[0]
            self.assertEqual(data1[0],(8,'Кукин','Куку','Кукуевич','Кукуево')[0])
            self.assertEqual(data1[1],(8,'Кукин','Куку','Кукуевич','Кукуево')[1])
            self.assertEqual(data1[2],(8,'Кукин','Куку','Кукуевич','Кукуево')[2])
            self.assertEqual(data1[3],(8,'Кукин','Куку','Кукуевич','Кукуево')[3])
            self.assertEqual(data1[4],(8,'Кукин','Куку','Кукуевич','Кукуево')[4])

    def test_sql_update_negative(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            Author.get_data()
            data1 = Author.content[0]
            Author.sql_update(2,'Идентификатор',1,new_window,scrollable_frame,root)
            Author.sql_update(8, 'Фамилия', 'Кукин+', new_window, scrollable_frame, root)
            Author.sql_update(8, 'Имя', 'Куку+', new_window, scrollable_frame, root)
            Author.sql_update(8, 'Отчество', 'Кукуевич+', new_window, scrollable_frame, root)
            Author.sql_update(8, 'Страна', 'Кукуев+', new_window, scrollable_frame, root)
            Author.get_data()
            data2 = Author.content[0]
            self.assertEqual(data1[0],data2[0])
            self.assertEqual(data1[1],data2[1])
            self.assertEqual(data1[2],data2[2])
            self.assertEqual(data1[3],data2[3])
            self.assertEqual(data1[4],data2[4])

    def test_show(self):
        root = tk.Tk()
        canvas = tk.Canvas(root)
        scrollable_frame = tk.Frame(canvas)
        Author.show_data(scrollable_frame, root)
        widgets = scrollable_frame.winfo_children()
        self.assertEqual('Авторы', widgets[0].cget('text'))
        self.assertEqual('Идентификатор', widgets[1].cget('text'))
        self.assertEqual('Фамилия', widgets[2].cget('text'))
        self.assertEqual('Имя', widgets[3].cget('text'))
        self.assertEqual('Отчество', widgets[4].cget('text'))
        self.assertEqual('Страна', widgets[5].cget('text'))
        self.assertEqual(2, widgets[6].cget('text'))
        self.assertEqual('Сандерсон', widgets[7].cget('text'))
        self.assertEqual('Брендон', widgets[8].cget('text'))
        self.assertEqual('', widgets[9].cget('text'))
        self.assertEqual('США', widgets[10].cget('text'))
        self.assertEqual('Удалить запись', widgets[11].cget('text'))
        self.assertTrue(isinstance(widgets[11], tk.Button))
        self.assertEqual('Добавить запись', widgets[30].cget('text'))
        self.assertTrue(isinstance(widgets[30], tk.Button))

    def test_update(self):
        root = tk.Tk()
        canvas = tk.Canvas(root)
        scrollable_frame = tk.Frame(canvas)
        Author.update(4, 1, 'Имя', root, scrollable_frame)
        widgets = root.winfo_children()[-1].winfo_children()
        self.assertEqual("Новое значение 'Имя': ", widgets[0].cget('text'))
        self.assertEqual('Обновить', widgets[2].cget('text'))
        self.assertTrue(isinstance(widgets[1],tk.Entry))
        self.assertTrue(isinstance(widgets[2],ttk.Button))







