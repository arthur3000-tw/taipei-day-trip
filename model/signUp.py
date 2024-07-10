from pydantic import BaseModel, EmailStr

# 建立 signUpInfo 資料 model
class SignUpInfo(BaseModel):
    name: str
    email: EmailStr
    password: str

# 註冊帳號
def signUp(myDB, signUpInfo: SignUpInfo):
    # 資料庫查詢是否有此 email
    sql = "SELECT * FROM user WHERE email = %s"
    val = (signUpInfo.email,)
    result = myDB.query(sql, val)
    # 無重複 email
    if len(result) == 0:
        # 將密碼加密
        encodedPassword = encodePassword(signUpInfo.password)
        # 輸入資料庫
        sql = "INSERT INTO user (name, email, password) VALUES (%s, %s, %s)"
        val = (signUpInfo.name, signUpInfo.email, encodedPassword)
        result = myDB.insert(sql, val)
        # 輸入完成
        if result == 1:
            return OK(ok=True)
        # 輸入失敗
        else:
            raise ValueError()
    # 有重複 email
    else:
        raise ValueError()


