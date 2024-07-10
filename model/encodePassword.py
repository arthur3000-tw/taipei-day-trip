import bcrypt

# 密碼加密
# 輸入
# password: 密碼
# 輸出
# hash: 加密密碼
def encodePassword(password):
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash