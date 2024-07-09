from mysql.connector import pooling
import os
# 資料庫訊息
myDB = {
    "host": "localhost",
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASS"),
    "database": "taipei_day_trip"
}


# 建立連接池
cnxPool = pooling.MySQLConnectionPool(pool_name="myPool", pool_size=5, **myDB)
