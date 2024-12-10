import unittest
from Order import Order
from db_connection import DbConnection
import tkinter as tk
from tkinter import ttk
from unittest.mock import patch
import datetime


class TestOrder(unittest.TestCase):
    def setUp(self):
        DbConnection.connect_to_access_db(r'C:\Users\User\PycharmProjects\BookStoreByTI\DB.accdb')

    def test_get_data(self):
        Order.get_data()
        self.assertEqual(-846302226, Order.content[1][0])
        self.assertEqual(1, Order.content[1][1])
        self.assertEqual('Выдан', Order.content[1][2])
        self.assertEqual(1989085300, Order.content[1][3])
        self.assertEqual(datetime.datetime(2024, 11, 11,0,0), Order.content[1][4])
        self.assertEqual(datetime.datetime(2024, 12, 2, 16, 22, 20), Order.content[1][5])

        self.assertEqual(834450533, Order.content[0][0])
        self.assertEqual(1, Order.content[0][1])
        self.assertEqual('Выдан', Order.content[0][2])
        self.assertEqual(1989085300, Order.content[0][3])
        self.assertEqual(datetime.datetime(2024, 12, 1,0,0), Order.content[0][4])
        self.assertEqual(datetime.datetime(2024, 12, 9, 19, 41, 44), Order.content[0][5])

    def test_show_data(self):
        root = tk.Tk()
        canvas = tk.Canvas(root)
        scrollable_frame = tk.Frame(canvas)
        Order.show_data(scrollable_frame)
        widgets = scrollable_frame.winfo_children()
        self.assertEqual('Заказы', widgets[0].cget('text'))
        self.assertEqual('Идентификатор', widgets[1].cget('text'))
        self.assertEqual('Статус', widgets[2].cget('text'))
        self.assertEqual(834450533, widgets[3].cget('text'))
        self.assertEqual('Выдан', widgets[4].cget('text'))
        self.assertEqual('Подробнее', widgets[5].cget('text'))
        self.assertTrue(isinstance(widgets[5], tk.Button))



