from fastapi.responses import JSONResponse
import json
from model.user.UserModel import UserInfo
from model.order.OrderModel import GetOrderOutput, GetOrder, Trip, Contact
from model.booking.BookingModel import BookingAttraction
from model.ResponseModel import Error

# 取得訂單
# 輸入
# myDB
# userInfo
# orderNumber
# 輸出
# GetOrderOutput 資料
def getOrder(myDB, userInfo:UserInfo, orderNumber:str):
    sql = "SELECT booking.*, orders.*, \
         attraction.id as a_id, attraction.name as a_name, attraction.address as a_address, attraction.images as a_images \
         FROM orders \
         INNER JOIN booking ON booking.id = orders.booking_id \
         INNER JOIN attraction ON booking.attraction_id = attraction.id \
         WHERE orders.order_number = %s AND booking.user_id = %s"
    val = (orderNumber,userInfo.data.id)
    result = myDB.query(sql,val)
    if len(result) == 1:
        result = result[0]
        image = json.loads(result["a_images"])
        image = image["images"][0]
        return GetOrderOutput(data=GetOrder(number=orderNumber,price=result["price"],
                                            trip=Trip(attraction=BookingAttraction(id=result["a_id"],name=result["a_name"],address=result["a_address"],image=image),
                                                    date=result["date"],time=result["time"]),
                                            contact=Contact(name=result["contact_name"],email=result["contact_email"],phone=result["contact_phone"]),
                                            status=result["status"]))
    else:
        return JSONResponse(status_code=400, content=Error(error=True, message="輸入資料錯誤，未查詢到此訂單").model_dump())