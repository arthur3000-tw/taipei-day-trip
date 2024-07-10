from pydantic import BaseModel

# 建立 error 資料 model
class Error(BaseModel):
    error: bool
    message: str

# 建立 ok 資料 model
class OK(BaseModel):
    ok: bool 
