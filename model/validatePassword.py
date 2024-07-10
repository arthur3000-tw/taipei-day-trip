import bcrypt

# 驗證密碼
# 輸入
# userPassword: 使用者輸入密碼
# dbPassword: 資料庫中密碼
# 輸出
# boolean
def validatePassword(userPassword, dbPassword):
    userPassword = userPassword.encode("utf-8")
    dbPassword = dbPassword.encode("utf-8")
    return bcrypt.checkpw(userPassword, dbPassword)
