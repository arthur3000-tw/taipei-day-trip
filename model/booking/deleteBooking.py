from fastapi.responses import JSONResponse
from model.user.UserModel import UserInfo
from model.ResponseModel import Error, OK

# 刪除 booking 資料
def deleteBooking(myDB, userInfo: UserInfo):
    # 取出資料
    userId = userInfo.data.id
    # 資料庫指令
    sql = "DELETE FROM booking WHERE user_id = %s and ordered = %s"
    val = (userId,False)
    result = myDB.insert(sql, val)
    if result != 0:
        return OK(ok=True)
    else:
        return JSONResponse(status_code=400, content=Error(error=True, message="沒有可以刪除的資料").model_dump())