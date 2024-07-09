import jwt
import datetime
from model.UserModel import UserInfo, User

class myJWT:
    def __init__(self, jwt_secret_key, expired_days, jwt_algorithm) -> None:
        # jwt 加密參數
        self.jwt_secret_key = jwt_secret_key
        self.expired_days = expired_days
        self.jwt_algorithm = jwt_algorithm
    # 驗證 JWT
    # 輸入
    # token: JWT
    # 輸出
    # UserInfo 資料
    def validate(self, token):
        try:
            result = jwt.decode(token, self.jwt_secret_key, algorithms=[self.jwt_algorithm])
            return UserInfo(data=User(id=result["id"], name=result["name"], email=result["email"]))
        except:
            return UserInfo(User=None)
    # 製作 JWT
    # 輸入
    # payload: 加密資料
    # days: 有效期限天數
    # 輸出
    # encoded_jwt: JWT
    def generate(self, payload, days):
        exp = datetime.datetime.now(
            tz=datetime.timezone.utc) + datetime.timedelta(days=days)
        payload["exp"] = exp
        encoded_jwt = jwt.encode(payload, self.jwt_secret_key, algorithm=self.jwt_algorithm)
        return encoded_jwt