from fastapi.responses import JSONResponse
from model.getAttractionById import get_attraction_id
from model.UserModel import UserInfo
from model.BookingModel import BookingOutput, Booking, BookingAttraction
from model.ResponseModel import Error


# 取得 booking 資料
# 輸入
# myDB
# userInfo
# 輸出
# Booking 資料
def getBooking(myDB, userInfo: UserInfo):
    # 取出資料
    userId = userInfo.data.id
    # 資料庫指令
    sql = "SELECT * FROM booking WHERE user_id = %s AND ordered = %s ORDER BY log_time DESC LIMIT 1"
    val = (userId,False)
    result = myDB.query(sql, val)
    if len(result) == 1:
        # 取出 booking 資料
        attractionId = result[0]["attraction_id"]
        date = result[0]["date"]
        time = result[0]["time"]
        price = result[0]["price"]
        # 取得 attraction 資料
        attractionInfo = get_attraction_id(attractionId)
        # 取出 bookingAttraction 資料
        attractionName = attractionInfo.data.name
        attractionAddress = attractionInfo.data.address
        attractionImage = attractionInfo.data.images[0]
        return BookingOutput(data=Booking(attraction=BookingAttraction(id=attractionId, name=attractionName, address=attractionAddress, image=attractionImage),
                                          date=date, time=time, price=price))
    else:
        return JSONResponse(status_code=400, content=Error(error=True, message="沒有符合的資料").model_dump())
