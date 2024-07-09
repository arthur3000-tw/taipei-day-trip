from pydantic import BaseModel, EmailStr

# 建立 user 資料 model
class User(BaseModel):
    id: int | None
    name: str | None
    email: EmailStr | None

# 建立 userInfo 資料 model
class UserInfo(BaseModel):
    data: User | None = None