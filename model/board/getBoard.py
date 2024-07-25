def get_board(myDB):
    sql = "SELECT * FROM board ORDER BY log_time DESC LIMIT 10"
    result = myDB.query(sql)
    return result