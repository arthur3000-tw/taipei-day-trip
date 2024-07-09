from mysql.connector import pooling
import os

class db:
    def __init__(self, host, database):
        self.host = host
        self.database = database
        self.cnxPool = None
    def initialize(self):
        # 資料庫訊息
        myDB = {
            "host": self.host,
            "user": os.environ.get("DB_USER"),
            "password": os.environ.get("DB_PASS"),
            "database": self.database
        }
        # 建立連接池
        self.cnxPool = pooling.MySQLConnectionPool(pool_name="myPool", pool_size=5, **myDB)

