import datetime
from model.booking.deleteBooking import deleteBooking
from model.user.UserModel import UserInfo
from model.order.OrderModel import OrderInput
from model.StatusModel import Status

def orderBooking(myDB, userInfo: UserInfo,orderInput:OrderInput):
    # 取出資料
    userId = userInfo.data.id
    attractionId = orderInput.order.trip.attraction.id
    date = orderInput.order.trip.date
    time = orderInput.order.trip.time
    # 取得 bookingId
    sql = "SELECT * FROM booking WHERE user_id = %s AND attraction_id = %s AND date = %s AND time = %s AND ordered = %s"
    val = (userId,attractionId,date,time,False)
    result = myDB.query(sql, val)
    if len(result) == 1:
        bookingId = result[0]["id"]
    else:
        return Status(status_code=1)
    # 更新 bookingId status
    log_time = datetime.datetime.now()
    sql = "UPDATE booking SET log_time = %s, ordered = %s \
         WHERE user_id = %s AND attraction_id = %s AND date = %s AND time = %s AND ordered = %s"
    val = (log_time,True,userId,attractionId,date,time,False)
    result = myDB.insert(sql, val)
    if result == 1:
        # 刪除其餘 booking
        delete_result = deleteBooking(myDB, userInfo)
        try:
            if delete_result.ok == True:
                return Status(status_code=0,data=bookingId)
        # 若無其他 booking 也是可以繼續
        except:
            return Status(status_code=3,data=bookingId)
    else:
        return Status(status_code=2)