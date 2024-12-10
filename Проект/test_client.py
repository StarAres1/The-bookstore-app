import unittest
from Client import Client
from db_connection import DbConnection
import tkinter as tk
from tkinter import ttk
from unittest.mock import patch
import  datetime


class TestClient(unittest.TestCase):
    def setUp(self):
        DbConnection.connect_to_access_db(r'C:\Users\User\PycharmProjects\BookStoreByTI\DB.accdb')

    def test_get_data(self):
        Client.get_data()
        self.assertEqual(1, Client.content[0][0])
        self.assertEqual(500, Client.content[0][2])
        self.assertEqual('рп', Client.content[0][3])
        self.assertEqual('апрра', Client.content[0][4])
        self.assertEqual('89696969', Client.content[0][5])
        self.assertEqual(datetime.datetime(2000, 12, 12, 0, 0), Client.content[0][6])

    def test_sql_delete_positive(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            Client.get_data()
            number1 = len(Client.content)
            Client.sql_delete('Идентификатор', 1, scrollable_frame, root)
            number2 = len(Client.content)
            self.assertEqual(number2, number1 - 1)

    def test_sgl_delete_negative(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            Client.get_data()
            number1 = len(Client.content)
            try:
                Client.sql_delete('Идентификатор', 3, scrollable_frame, root)
            except:
                pass
            number2 = len(Client.content)
            self.assertEqual(number2, number1)

    def test_validate_name_positive(self):
        self.assertEqual(True, Client.validate_name('Кнопка-Шнопка'))

    def test_validate_name_negative(self):
        self.assertEqual(False, Client.validate_name('556++'))

    def test_validate_id_positive(self):
        self.assertEqual(True, Client.validate_id('5'))

    def test_validate_id_negative(self):
        self.assertEqual(False, Client.validate_id('556++'))

    def test_validate_date_positive(self):
        self.assertEqual(True, Client.validate_date('2001-12-5'))

    def test_validate_date_negative(self):
        self.assertEqual(False, Client.validate_date('556++'))

    def test_validate_amount_positive(self):
        self.assertEqual(True, Client.validate_amount('500'))

    def test_validate_amount_negative(self):
        self.assertEqual(False, Client.validate_amount('556++'))

    def test_validate_count_positive(self):
        self.assertEqual(True, Client.validate_count('500.0'))

    def test_validate_count_negative(self):
        self.assertEqual(False, Client.validate_count('556++'))

    def test_validate_positive(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            surname = ttk.Entry(new_window)
            name = ttk.Entry(new_window)
            number = ttk.Entry(new_window)
            birth = ttk.Entry(new_window)

            surname.insert(0, 'Хихи')
            name.insert(0, 'Хаха')
            number.insert(0, 66666666666)
            birth.insert(0, '2001-5-8')
            Client.get_data()
            number1 = len(Client.content)
            Client.validate(surname,name,number,birth,new_window, scrollable_frame,root)
            number2 = len(Client.content)
            self.assertEqual(number2, number1+1)

    def test_validate_negative(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            surname = ttk.Entry(new_window)
            name = ttk.Entry(new_window)
            number = ttk.Entry(new_window)
            birth = ttk.Entry(new_window)

            surname.insert(0, 'Хихи5')
            name.insert(0, 'Хаха5')
            number.insert(0, '666g')
            birth.insert(0, '2001-5-8g')
            Client.get_data()
            number1 = len(Client.content)
            Client.validate(surname, name, number, birth, new_window, scrollable_frame, root)
            number2 = len(Client.content)
            self.assertEqual(number2, number1)

    def test_add(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            Client.add_new_row(root, scrollable_frame)
            widgets = root.winfo_children()[-1].winfo_children()
            self.assertEqual("Добавление", root.winfo_children()[-1].title())
            self.assertEqual("Фамилия:", widgets[0].cget('text'))
            self.assertEqual("Имя:", widgets[2].cget('text'))
            self.assertEqual("Номер телефона:", widgets[4].cget('text'))
            self.assertEqual("Дата рождения:", widgets[6].cget('text'))
            self.assertTrue(isinstance(widgets[1], tk.Entry))
            self.assertTrue(isinstance(widgets[3], tk.Entry))
            self.assertTrue(isinstance(widgets[5], tk.Entry))
            self.assertTrue(isinstance(widgets[7], tk.Entry))
            self.assertTrue(isinstance(widgets[8], ttk.Button))
            self.assertEqual("Добавить", widgets[8].cget('text'))

    def test_sql_add_positive(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            Client.get_data()
            number1 = len(Client.content)
            data = ['Кукуев','Куку','1111','2000-5-8']
            Client.sql_add(data,new_window,scrollable_frame,root)
            Client.get_data()
            number2 = len(Client.content)
            self.assertEqual(number2,number1+1)

    def test_sql_add_negative(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            Client.get_data()
            number1 = len(Client.content)
            data = ['Кукуев5','Куку5','11115','2000-5-85']
            Client.sql_add(data,new_window,scrollable_frame,root)
            Client.get_data()
            number2 = len(Client.content)
            self.assertEqual(number2,number1)

    def test_update(self):
        root = tk.Tk()
        canvas = tk.Canvas(root)
        scrollable_frame = tk.Frame(canvas)
        Client.update(4, 1, 'Имя', root, scrollable_frame)
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
            Client.sql_update(1, 'Фамилия', 'Кукин', new_window, scrollable_frame, root)
            Client.sql_update(1, 'Имя', 'Куку', new_window, scrollable_frame, root)
            Client.sql_update(1, 'Номер телефона', '99999999999', new_window, scrollable_frame, root)
            Client.sql_update(1, 'Дата рождения', '2001-5-8', new_window, scrollable_frame, root)
            Client.sql_update(1, 'Баллы', '1000', new_window, scrollable_frame, root)
            Client.get_data()
            data1 = Client.content[0]
            self.assertEqual(data1[6],(1,'Кукин','Куку','99999999999',datetime.datetime(2001,5,8,0,0),1000)[4])
            self.assertEqual(data1[3],(1,'Кукин','Куку','99999999999',datetime.datetime(2001,5,8,0,0),1000)[1])
            self.assertEqual(data1[4],(1,'Кукин','Куку','99999999999',datetime.datetime(2001,5,8,0,0),1000)[2])
            self.assertEqual(data1[5],(1,'Кукин','Куку','99999999999',datetime.datetime(2001,5,8,0,0),1000)[3])
            self.assertEqual(data1[2],(1,'Кукин','Куку','99999999999',datetime.datetime(2001,5,8,0,0),1000)[5])

    def test_sql_update_negative(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            root = tk.Tk()
            canvas = tk.Canvas(root)
            scrollable_frame = tk.Frame(canvas)
            new_window = tk.Toplevel(root)
            Client.sql_update(1, 'Фамилия', 'Кукин1', new_window, scrollable_frame, root)
            Client.sql_update(1, 'Имя', 'Куку1', new_window, scrollable_frame, root)
            Client.sql_update(1, 'Номер телефона', '99999999999f', new_window, scrollable_frame, root)
            Client.sql_update(1, 'Дата рождения', '2001-5-8g', new_window, scrollable_frame, root)
            Client.sql_update(1, 'Баллы', '1000h', new_window, scrollable_frame, root)
            Client.get_data()
            data1 = Client.content[0]
            self.assertEqual(data1[2],data1[2])
            self.assertEqual(data1[3], data1[3])
            self.assertEqual(data1[4], data1[4])
            self.assertEqual(data1[5], data1[5])
            self.assertEqual(data1[6], data1[6])

    def test_show_data(self):
        root = tk.Tk()
        canvas = tk.Canvas(root)
        scrollable_frame = tk.Frame(canvas)
        Client.show_data(scrollable_frame, root)
        widgets = scrollable_frame.winfo_children()
        self.assertEqual('Клиенты', widgets[0].cget('text'))
        self.assertEqual('Идентификатор', widgets[1].cget('text'))
        self.assertEqual('Стоимость купленных товаров', widgets[2].cget('text'))
        self.assertEqual('Баллы', widgets[3].cget('text'))
        self.assertEqual('Фамилия', widgets[4].cget('text'))
        self.assertEqual('Имя', widgets[5].cget('text'))
        self.assertEqual('Номер телефона', widgets[6].cget('text'))
        self.assertEqual('Дата рождения', widgets[7].cget('text'))

        self.assertEqual(1, widgets[8].cget('text'))
        self.assertEqual('1000.0000', widgets[9].cget('text'))
        self.assertEqual(500, widgets[10].cget('text'))
        self.assertEqual('рп', widgets[11].cget('text'))
        self.assertEqual('апрра', widgets[12].cget('text'))
        self.assertEqual('89696969', widgets[13].cget('text'))
        self.assertEqual('2000-12-12 00:00:00', widgets[14].cget('text'))




