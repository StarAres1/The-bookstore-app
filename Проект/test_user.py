import unittest
from User import User
from db_connection import DbConnection
import tkinter as tk
from tkinter import ttk
from unittest.mock import patch
import  datetime


class TestUser(unittest.TestCase):
    def setUp(self):
        DbConnection.connect_to_access_db(r'C:\Users\User\PycharmProjects\BookStoreByTI\DB.accdb')

    def test_get_data(self):
        User.get_data()
        self.assertEqual(1989085300, User.content[0][0])
        self.assertEqual('Тетерин',User.content[0][1])
        self.assertEqual('Андрей',User.content[0][2])
        self.assertEqual('Сергеевич',User.content[0][3])
        self.assertEqual(datetime.datetime(2022,11,11,0,0),User.content[0][4])
        self.assertEqual('1',User.content[0][5])

    def test_sql_delete_positive(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            User.get_data()
            number1 = len(User.content)
            User.sql_delete('Идентификатор', 1733148862, scrollable_frame, root)
            number2 = len(User.content)
            self.assertEqual(number2, number1 - 1)

    def test_sgl_delete_negative(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            User.get_data()
            number1 = len(User.content)
            try:
                User.sql_delete('Идентификатор', 3, scrollable_frame, root)
            except:
                pass
            number2 = len(User.content)
            self.assertEqual(number2, number1)

    def test_validate_name_positive(self):
        self.assertEqual(True, User.validate_name('Кнопка-Шнопка'))

    def test_validate_name_negative(self):
        self.assertEqual(False, User.validate_name('556++'))

    def test_validate_id_positive(self):
        self.assertEqual(True, User.validate_id('5'))

    def test_validate_id_negative(self):
        self.assertEqual(False, User.validate_id('556++'))

    def test_validate_status_positive(self):
        self.assertEqual(True, User.validate_status('1'))

    def test_validate_status_negative(self):
        self.assertEqual(False, User.validate_status('556++'))

    def test_validate_date_positive(self):
        self.assertEqual(True, User.validate_date('2001-12-5'))

    def test_validate_date_negative(self):
        self.assertEqual(False, User.validate_date('556++'))

    def test_validate_positive(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            surname = ttk.Entry(new_window)
            name = ttk.Entry(new_window)
            last = ttk.Entry(new_window)
            birth = ttk.Entry(new_window)
            password = ttk.Entry(new_window)
            status = ttk.Entry(new_window)

            surname.insert(0, 'Хихи')
            name.insert(0, 'Хаха')
            last.insert(0, 'Хохо')
            birth.insert(0, '2001-5-8')
            password.insert(0, '2222')
            status.insert(0, '2')
            User.get_data()
            number1 = len(User.content)
            User.validate(surname,name,last,birth, password,status, new_window, scrollable_frame,root)
            number2 = len(User.content)
            self.assertEqual(number2, number1+1)

    def test_validate_negative(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            surname = ttk.Entry(new_window)
            name = ttk.Entry(new_window)
            last = ttk.Entry(new_window)
            birth = ttk.Entry(new_window)
            password = ttk.Entry(new_window)
            status = ttk.Entry(new_window)

            surname.insert(0, 'Хихи1')
            name.insert(0, 'Хаха1')
            last.insert(0, 'Хохо1')
            birth.insert(0, '2001-5-88')
            password.insert(0, '2222')
            status.insert(0, '3')
            User.get_data()
            number1 = len(User.content)
            User.validate(surname, name, last, birth, password, status, new_window, scrollable_frame, root)
            number2 = len(User.content)
            self.assertEqual(number2, number1)

    def test_add(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            User.add_new_row(root, scrollable_frame)
            widgets = root.winfo_children()[-1].winfo_children()
            self.assertEqual("Добавление", root.winfo_children()[-1].title())
            self.assertEqual("Фамилия:", widgets[0].cget('text'))
            self.assertEqual("Имя:", widgets[2].cget('text'))
            self.assertEqual("Отчество (н/о):", widgets[4].cget('text'))
            self.assertEqual("Дата рождения (ГГГГ-ММ-ДД)", widgets[6].cget('text'))
            self.assertEqual("Пароль: ", widgets[8].cget('text'))
            self.assertEqual("Уровень(1/2): ", widgets[10].cget('text'))
            self.assertTrue(isinstance(widgets[1], tk.Entry))
            self.assertTrue(isinstance(widgets[3], tk.Entry))
            self.assertTrue(isinstance(widgets[5], tk.Entry))
            self.assertTrue(isinstance(widgets[7], tk.Entry))
            self.assertTrue(isinstance(widgets[9], tk.Entry))
            self.assertTrue(isinstance(widgets[11], tk.Entry))
            self.assertTrue(isinstance(widgets[12], ttk.Button))
            self.assertEqual("Добавить", widgets[12].cget('text'))

    def test_sql_add_positive(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            User.get_data()
            number1 = len(User.content)
            data = ['Кукуев','Куку','Кук','2000-5-8','1111','2']
            User.sql_add(data,new_window,scrollable_frame,root)
            User.get_data()
            number2 = len(User.content)
            self.assertEqual(number2,number1+1)

    def test_sql_add_negative(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            User.get_data()
            number1 = len(User.content)
            data = ['Кукуев5','Куку5','Кук5','2000-5-89','1111','28']
            User.sql_add(data,new_window,scrollable_frame,root)
            User.get_data()
            number2 = len(User.content)
            self.assertEqual(number2,number1)

    def test_update(self):
        root = tk.Tk()
        canvas = tk.Canvas(root)
        scrollable_frame = tk.Frame(canvas)
        User.update(4, 1, 'Имя', root, scrollable_frame)
        widgets = root.winfo_children()[-1].winfo_children()
        self.assertEqual("Новое значение 'Имя': ", widgets[0].cget('text'))
        self.assertEqual('Обновить', widgets[2].cget('text'))
        self.assertTrue(isinstance(widgets[1],tk.Entry))
        self.assertTrue(isinstance(widgets[2],ttk.Button))

    def test_sql_update_positive(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            User.sql_update(1989085300, 'Фамилия', 'Кукин', new_window, scrollable_frame, root)
            User.sql_update(1989085300, 'Имя', 'Куку', new_window, scrollable_frame, root)
            User.sql_update(1989085300, 'Отчество', 'Кукуевич', new_window, scrollable_frame, root)
            User.sql_update(1989085300, 'Дата рождения', '2001-5-8', new_window, scrollable_frame, root)
            User.sql_update(1989085300, 'Уровень привелегий', '1', new_window, scrollable_frame, root)
            User.get_data()
            data1 = User.content[0]
            self.assertEqual(data1[0],(1989085300,'Кукин','Куку','Кукуевич',datetime.datetime(2001,5,8,0,0),'1')[0])
            self.assertEqual(data1[1],(1989085300,'Кукин','Куку','Кукуевич',datetime.datetime(2001,5,8,0,0),'1')[1])
            self.assertEqual(data1[2],(1989085300,'Кукин','Куку','Кукуевич',datetime.datetime(2001,5,8,0,0),'1')[2])
            self.assertEqual(data1[3],(1989085300,'Кукин','Куку','Кукуевич',datetime.datetime(2001,5,8,0,0),'1')[3])
            self.assertEqual(data1[4],(1989085300,'Кукин','Куку','Кукуевич',datetime.datetime(2001,5,8,0,0),'1')[4])

    def test_sql_update_negative(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            User.get_data()
            data1 = User.content[0]
            User.sql_update(2,'Идентификатор',1,new_window,scrollable_frame,root)
            User.sql_update(8, 'Фамилия', 'Кукин+', new_window, scrollable_frame, root)
            User.sql_update(8, 'Имя', 'Куку+', new_window, scrollable_frame, root)
            User.sql_update(8, 'Отчество', 'Кукуевич+', new_window, scrollable_frame, root)
            User.sql_update(8, 'Дата рождения', 'Кукуев+', new_window, scrollable_frame, root)
            User.sql_update(8, 'Уровень привелегий', 'Кукуев+', new_window, scrollable_frame, root)
            User.get_data()
            data2 = User.content[0]
            self.assertEqual(data1[0],data2[0])
            self.assertEqual(data1[1],data2[1])
            self.assertEqual(data1[2],data2[2])
            self.assertEqual(data1[3],data2[3])
            self.assertEqual(data1[4],data2[4])

    def test_show(self):
        root = tk.Tk()
        canvas = tk.Canvas(root)
        scrollable_frame = tk.Frame(canvas)
        User.show_data(scrollable_frame, root)
        widgets = scrollable_frame.winfo_children()
        self.assertEqual('Пользователи', widgets[0].cget('text'))
        self.assertEqual('Идентификатор', widgets[1].cget('text'))
        self.assertEqual('Фамилия', widgets[2].cget('text'))
        self.assertEqual('Имя', widgets[3].cget('text'))
        self.assertEqual('Отчество', widgets[4].cget('text'))
        self.assertEqual('Дата рождения', widgets[5].cget('text'))
        self.assertEqual('Уровень привелегий', widgets[6].cget('text'))
        self.assertEqual(1989085300, widgets[7].cget('text'))
        self.assertEqual('Тетерин', widgets[8].cget('text'))
        self.assertEqual('Андрей', widgets[9].cget('text'))
        self.assertEqual('Сергеевич', widgets[10].cget('text'))
        self.assertEqual('2022-11-11 00:00:00', widgets[11].cget('text'))
        self.assertEqual('1', widgets[12].cget('text'))
        self.assertEqual('Удалить запись', widgets[13].cget('text'))
        self.assertTrue(isinstance(widgets[13], tk.Button))




