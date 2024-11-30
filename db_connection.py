import pyodbc

class DbConnection:

    cursor = None
    conn = None
    @staticmethod
    def connect_to_access_db(db_file: str):
        connection_string = rf'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_file};'
        DbConnection.conn = pyodbc.connect(connection_string)
        DbConnection.cursor = DbConnection.conn.cursor()

    @staticmethod
    def close_connection():
        DbConnection.conn.close()
