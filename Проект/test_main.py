import unittest
from unittest.mock import MagicMock, patch
from application import Main
import tkinter as tk
from tkinter import messagebox, ttk


class TestMain(unittest.TestCase):
    def setUp(self):
        self.approot = tk.Tk()
        self.app = Main(self.approot)

    def TearDown(self):
        self.app.master.destroy()

    def test_start(self):
        widgets = self.app.master.winfo_children()

        self.assertEqual(self.app.master.title, "Система магазина")


if __name__ == '__main__':
    unittest.main()
