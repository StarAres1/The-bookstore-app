import pyodbc

class DbConnection:

    cursor = None
    conn = None
    @staticmethod
    def connect_to_access_db(db_file: str):
        try:
            connection_string = rf'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_file};'
            DbConnection.conn = pyodbc.connect(connection_string)
            DbConnection.cursor = DbConnection.conn.cursor()
            return True
        except:
            return False

    @staticmethod
    def commit():
        DbConnection.conn.commit()

    @staticmethod
    def close_connection():
        try:
            DbConnection.conn.close()
            return True
        except:
            return False