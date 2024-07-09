import jwt

# 驗證 JWT
# 輸入
# token: JWT
# 輸出
# UserInfo 資料
def validateJWT(token):
    try:
        result = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return UserInfo(data=User(id=result["id"], name=result["name"], email=result["email"]))
    except:
        return UserInfo(User=None)