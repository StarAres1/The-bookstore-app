import unittest
from db_connection import DbConnection


class TestConnection(unittest.TestCase):
    def setUp(self):
        pass

    def test_set_connection(self):
        self.assertEqual(True, DbConnection.connect_to_access_db(r'C:\Users\User\PycharmProjects\BookStoreByTI\DB.accdb'))
        self.assertEqual(False,
                         DbConnection.connect_to_access_db(r'C:\Users\User\PycharmProjects\BookStoreByTI\DB.accd'))

    def test_close_connection(self):
        self.assertEqual(False, DbConnection.close_connection())
        DbConnection.connect_to_access_db(r'C:\Users\User\PycharmProjects\BookStoreByTI\DB.accdb')
        self.assertEqual(True, DbConnection.close_connection())


if __name__ == '__main__':
    unittest.main()
