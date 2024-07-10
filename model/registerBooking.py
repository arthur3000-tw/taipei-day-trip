from fastapi.responses import JSONResponse
from model.isBookingRegistered import isBookingRegistered
from model.ResponseModel import Error, OK
from model.BookingModel import BookingInput
from model.UserModel import UserInfo

# 記錄 booking 狀況
# 輸入
# bookingInput
# userInfo
# 輸出
def registerBooking(myDB, bookingInput: BookingInput, userInfo: UserInfo):
    # 確認 booking 狀況
    # 若已經有重複 booking 狀況
    if isBookingRegistered(myDB, bookingInput, userInfo):
        result = updateBooking(myDB, bookingInput, userInfo)
        if result.status_code == 0:
            return JSONResponse(status_code=400, content=Error(error=True, message="重複預訂行程").model_dump())
        else:
            return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤").model_dump())
    # 沒有重複 booking 狀況
    else:
        # 取出資料
        userId = userInfo.data.id
        attractionId = bookingInput.attractionId
        date = bookingInput.date
        time = bookingInput.time
        price = bookingInput.price
        # 資料庫指令
        sql = "INSERT INTO booking (user_id, attraction_id, date, time, price) \
               VALUES (%s,%s,%s,%s,%s)"
        val = (userId, attractionId, date, time, price)
        result = myDB.insert(sql, val)
        if result == 1:
            return OK(ok=True)
        else:
            return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤").model_dump())