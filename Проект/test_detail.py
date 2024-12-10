import unittest
from Detail import Detail
from db_connection import DbConnection
import datetime
import tkinter as tk
from unittest.mock import patch


class TestDetail(unittest.TestCase):
    def setUp(self):
        DbConnection.connect_to_access_db(r'C:\Users\User\PycharmProjects\BookStoreByTI\DB.accdb')

    def test_get_data(self):
        data_of_order = [834450533, 1, 'Отменён', 1989085300, datetime.datetime(2024, 11, 11), '']
        Detail.get_data(data_of_order)
        self.assertEqual("рп", Detail.content_buyer[0][0])
        self.assertEqual('апрра', Detail.content_buyer[0][1])
        self.assertEqual(datetime.datetime(2000, 12, 12), Detail.content_buyer[0][2])
        self.assertEqual('89696969', Detail.content_buyer[0][3])

        self.assertEqual(834450533, Detail.content_order[0])
        self.assertEqual(1, Detail.content_order[1])
        self.assertEqual('Отменён', Detail.content_order[2])
        self.assertEqual(1989085300, Detail.content_order[3])
        self.assertEqual(datetime.datetime(2024, 11, 11), Detail.content_order[4])
        self.assertEqual('', Detail.content_order[5])

        self.assertEqual(120, Detail.content_details[0][0])
        self.assertEqual(2, Detail.content_details[0][1])
        self.assertEqual(100, Detail.content_details[0][2])
        self.assertEqual(121, Detail.content_details[1][0])
        self.assertEqual(1, Detail.content_details[1][1])
        self.assertEqual(500, Detail.content_details[1][2])

    def test_cancel(self):
        with patch.object(DbConnection, 'commit') as mock_commit:
            data_of_order = [834450533, 1, 'Выдан', 1989085300, datetime.datetime(2024, 11, 11), '']
            Detail.get_data(data_of_order)
            query = "SELECT Количество FROM Книги WHERE ISBN = ?;"
            DbConnection.cursor.execute(query, (Detail.content_details[0][0],))
            number1 = DbConnection.cursor.fetchone()[0]
            frame = tk.Tk()
            label = tk.Label(frame, text=Detail.content_order[2], fg="black", font=("Arial", 16, "bold"))
            Detail.cancel(label)
            self.assertEqual(label.cget('text'), 'Отменен')
            query = "SELECT Количество FROM Книги WHERE ISBN = ?;"
            DbConnection.cursor.execute(query, (Detail.content_details[0][0],))
            number2 = DbConnection.cursor.fetchone()[0]
            self.assertEqual(Detail.content_details[0][1],number2-number1)

    def test_high(self):
        frame = tk.Tk()
        data_of_order = [834450533, 1, 'Создан', 1989085300, datetime.datetime(2024, 11, 11), '']
        Detail.get_data(data_of_order)
        label1 = tk.Label(frame, text=Detail.content_order[2], fg="black", font=("Arial", 16, "bold"))
        label2 = tk.Label(frame, text=Detail.content_order[5], fg="black", font=("Arial", 16, "bold"))
        Detail.high(label1, label2)
        self.assertEqual('Собран', label1.cget('text'))
        self.assertEqual('', label2.cget('text'))
        Detail.high(label1, label2)
        self.assertEqual('Выдан', label1.cget('text'))
        self.assertEqual(26, len(label2.cget('text')))

    def test_show(self):
        frame = tk.Tk()
        data_of_order = [834450533, 1, 'Выдан', 1989085300, datetime.datetime(2024, 11, 11), '']
        Detail.show_data(frame, data_of_order)
        widgets = frame.winfo_children()
        self.assertEqual(f"Заказ N{data_of_order[0]}",widgets[0].cget('text'))

        self.assertEqual("Информация о покупателе", widgets[1].cget('text'))
        self.assertEqual("Фамилия:", widgets[2].cget('text'))
        self.assertEqual(Detail.content_buyer[0][0], widgets[3].cget('text'))
        self.assertEqual("Имя:", widgets[4].cget('text'))
        self.assertEqual(Detail.content_buyer[0][1], widgets[5].cget('text'))
        self.assertEqual("Номер телефона: ", widgets[6].cget('text'))
        self.assertEqual(Detail.content_buyer[0][3], widgets[7].cget('text'))
        self.assertEqual("Дата рождения:", widgets[8].cget('text'))
        self.assertEqual(str(Detail.content_buyer[0][2].year)+'-'+str(Detail.content_buyer[0][2].month)+'-'
                         +str(Detail.content_buyer[0][2].day), widgets[9].cget('text')[:10])

        self.assertEqual("Состав заказа", widgets[10].cget('text'))
        self.assertEqual("Идентификатор товара", widgets[11].cget('text'))
        self.assertEqual("Количество", widgets[12].cget('text'))
        self.assertEqual("Цена", widgets[13].cget('text'))


if __name__ == '__main__':
    unittest.main()
