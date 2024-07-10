from model.UserModel import UserAuth
from model.MyJWT import JWT
from model.validatePassword import validatePassword

# 驗證使用者
# 輸入
# userAuth 格式資料
# 輸出
# 密碼正確： JWT 格式資料
# 密碼錯誤： ValueError()
def validateUser(myDB, my_jwt, userAuth: UserAuth):
    # 資料庫查詢是否有此 email
    sql = "SELECT * FROM user WHERE email = %s"
    val = (userAuth.email,)
    result = myDB.query(sql, val)
    # 有找到此 email 且密碼正確
    if len(result) == 1 and validatePassword(userAuth.password, result[0]["password"]):
        # 進行製作 JWT，設置七天時間期限
        payload = {"id": result[0]["id"], "name": result[0]
                   ["name"], "email": result[0]["email"]}
        return JWT(token=my_jwt.generate(payload))
    # 未找到此 email 或密碼錯誤
    else:
        raise ValueError()