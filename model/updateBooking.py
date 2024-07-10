import datetime
from model.BookingModel import BookingInput
from model.UserModel import UserInfo
from model.StatusModel import Status

# 更新 booking 資料
# 輸入
# bookingInput
# userInfo
# 輸出 Status 資料
# status_code = 0 => 更新完成
# status_code = 1 => 錯誤
def updateBooking(myDB, bookingInput: BookingInput, userInfo: UserInfo):
    userId = userInfo.data.id
    attractionId = bookingInput.attractionId
    date = bookingInput.date
    time = bookingInput.time
    log_time = datetime.datetime.now()
    # 更新資料庫資料
    sql = "UPDATE booking SET log_time = %s \
         WHERE user_id = %s AND attraction_id = %s AND date = %s AND time = %s"
    val = (log_time, userId, attractionId, date, time)
    result = myDB.insert(sql, val)
    if result == 1:
        return Status(status_code=0)
    else:
        return Status(status_code=1)