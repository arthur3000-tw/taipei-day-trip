from mysql.connector import pooling
import os

class DB:
    def __init__(self, host, database):
        self.host = host
        self.database = database
        self.cnxPool = None
    # 初始化資料庫，建立 pool 連線
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
    # 向資料庫查詢
    # 輸入
    # sql: str      資料庫指令
    # val: str      查詢內容
    # 輸出
    # myResult      查詢結果
    def query(self,sql, val=None):
        # 從連接池取得連線
        cnx = self.cnxPool.get_connection()
        # 進行操作
        myCursor = cnx.cursor(dictionary=True)
        myCursor.execute(sql, val)
        myResult = myCursor.fetchall()
        # 關閉游標與連接
        myCursor.close()
        cnx.close()
        # 回傳結果
        return myResult
