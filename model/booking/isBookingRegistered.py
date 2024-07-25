from model.booking.BookingModel import BookingInput
from model.user.UserModel import UserInfo

# 確認 booking 資料
# 輸入
# BookingInput
# UserInfo
# 輸出
# boolean
def isBookingRegistered(myDB, bookingInput: BookingInput, userInfo: UserInfo):
    userId = userInfo.data.id
    attractionId = bookingInput.attractionId
    date = bookingInput.date
    time = bookingInput.time
    # 向資料庫取得資料
    sql = "SELECT * FROM booking WHERE user_id = %s AND attraction_id = %s AND date = %s AND time = %s AND ordered = %s"
    val = (userId, attractionId, date, time, False)
    result = myDB.query(sql, val)
    # 結果數量
    dataCounts = len(result)
    # dataCounts 數量為零（查無結果）
    if dataCounts == 0:
        return False
    else:
        return True
