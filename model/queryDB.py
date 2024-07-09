# 向資料庫查詢
# 輸入
# sql: str      資料庫指令
# val: str      查詢內容
# 輸出
# myResult      查詢結果
def queryDB(sql, val=None):
    # 從連接池取得連線
    cnx = cnxPool.get_connection()
    # 進行操作
    myCursor = cnx.cursor(dictionary=True)
    myCursor.execute(sql, val)
    myResult = myCursor.fetchall()
    # 關閉游標與連接
    myCursor.close()
    cnx.close()
    # 回傳結果
    return myResult