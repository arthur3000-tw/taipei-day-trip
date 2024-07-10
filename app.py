from controller import getAttractions, getAttractionById, getMrts, getUserAuth, putUserAuth, postUser, postBooking, getBooking
from controller import staticPage, httpExceptionHandler, validationExceptionHandler
from model import DB, MyJWT
import urllib.request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException
from typing import Annotated
from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, EmailStr
from enum import Enum, IntEnum
import json
import jwt
import bcrypt
import uuid
import datetime
import urllib
import os


# app 加入 dependencies
app = FastAPI()
app.mount('/static', StaticFiles(directory='static', html=True))


# DB 實體化
myDB = DB.DB(host="localhost",database="taipei_day_trip")
myDB.initialize()
# db instance 存放於 app.state 中
app.state.db = myDB




class Trip(BaseModel):
    attraction: BookingAttraction
    date: datetime.date
    time: TimeEnum


class Contact(BaseModel):
    name: str
    email: EmailStr
    phone: str


class Order(BaseModel):
    price: PriceEnum
    trip: Trip
    contact: Contact


class OrderInput(BaseModel):
    prime: str
    order: Order


class PrimeOutput(BaseModel):
    status: int
    message: str
    rec_trade_id: str | None = None
    transaction_time: datetime.datetime | None = None


class Payment(BaseModel):
    status: int
    message: str


class OrderInfo(BaseModel):
    number: str
    payment: Payment


class OrderOutput(BaseModel):
    data: OrderInfo


class GetOrder(BaseModel):
    number: str
    price: PriceEnum
    trip: Trip
    contact: Contact
    status: int


class GetOrderOutput(BaseModel):
    data: GetOrder


# 實體化 MyJWT
my_jwt = MyJWT.MyJWT(jwt_secret_key = os.environ.get("JWT_SECRET_KEY"), expired_days = 7, jwt_algorithm = "HS256")
# MyJWT instance 存放於 app.state 中
app.state.jwt = my_jwt


# 刪除 booking 資料
def deleteBooking(userInfo: UserInfo):
    # 取出資料
    userId = userInfo.data.id
    # 資料庫指令
    sql = "DELETE FROM booking WHERE user_id = %s and ordered = %s"
    val = (userId,False)
    result = insertDB(sql, val)
    if result != 0:
        return OK(ok=True)
    else:
        return JSONResponse(status_code=400, content=Error(error=True, message="沒有可以刪除的資料").model_dump())


def generateOrderNumber(primeOutput:PrimeOutput):
    today = datetime.datetime.now().strftime("%Y%m%d")
    string = primeOutput.rec_trade_id
    number = ""
    for ch in string[:8:-1]:
        number += str(ord(ch))
    number = today + number
    return number


def orderBooking(userInfo: UserInfo,orderInput:OrderInput):
    # 取出資料
    userId = userInfo.data.id
    attractionId = orderInput.order.trip.attraction.id
    date = orderInput.order.trip.date
    time = orderInput.order.trip.time
    # 取得 bookingId
    sql = "SELECT * FROM booking WHERE user_id = %s AND attraction_id = %s AND date = %s AND time = %s AND ordered = %s"
    val = (userId,attractionId,date,time,False)
    result = queryDB(sql, val)
    if len(result) == 1:
        bookingId = result[0]["id"]
    else:
        return Status(status_code=1)
    # 更新 bookingId status
    log_time = datetime.datetime.now()
    sql = "UPDATE booking SET log_time = %s, ordered = %s \
         WHERE user_id = %s AND attraction_id = %s AND date = %s AND time = %s AND ordered = %s"
    val = (log_time,True,userId,attractionId,date,time,False)
    result = insertDB(sql, val)
    if result == 1:
        # 刪除其餘 booking
        delete_result = deleteBooking(userInfo)
        try:
            if delete_result.ok == True:
                return Status(status_code=0,data=bookingId)
        # 若無其他 booking 也是可以繼續
        except:
            return Status(status_code=3,data=bookingId)
    else:
        return Status(status_code=2)


def registerOrder(orderInput: OrderInput, userInfo: UserInfo):
    # TapPay order
    primeOutput = payByPrime(orderInput)
    if primeOutput.status != 0:
        return JSONResponse(status_code=400, content=Error(error=True, message="付款失敗").model_dump())
    # Generate order number
    orderNumber = generateOrderNumber(primeOutput)
    # Get booking id and change status
    status = orderBooking(userInfo,orderInput)
    if status.status_code == 1:
        return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤，未找到此訂單(1)").model_dump())
    elif status.status_code == 2:
        return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤，未找到此訂單(2)").model_dump())
    elif status.status_code == 3:
        pass
    # 資料庫
    sql = "INSERT INTO orders (booking_id,status,message,trade_id,transaction_time,order_number,contact_name,contact_email,contact_phone) \
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (status.data,primeOutput.status,primeOutput.message,primeOutput.rec_trade_id,primeOutput.transaction_time,orderNumber,
           orderInput.order.contact.name,orderInput.order.contact.email,orderInput.order.contact.phone)
    result = insertDB(sql,val)
    if result == 1:
        return OrderOutput(data=OrderInfo(number=orderNumber,payment=Payment(status=primeOutput.status,message=primeOutput.message)))
    else:
        return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤").model_dump())


def payByPrime(orderInput: OrderInput):
    #
    url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": os.environ.get("PARTNER_KEY"),
    }
    data = json.dumps({
        "prime": orderInput.prime,
        "partner_key": os.environ.get("PARTNER_KEY"),
        "merchant_id": "arthur3000_ESUN",
        "details": "TapPay Test",
        "amount": orderInput.order.price,
        "cardholder": {
            "phone_number": orderInput.order.contact.phone,
            "name": orderInput.order.contact.name,
            "email": orderInput.order.contact.email,
        },
    }).encode()
    #
    request = urllib.request.Request(url=url, headers=headers, data=data)
    #
    with urllib.request.urlopen(request) as response:
        response_body = json.loads(response.read().decode("utf-8"))
    #
    status = response_body["status"]
    message = response_body["msg"]
    rec_trade_id = response_body["rec_trade_id"]
    transaction_time = datetime.datetime.fromtimestamp(response_body["transaction_time_millis"]/1000)
    #
    return PrimeOutput(status=status,message=message,rec_trade_id=rec_trade_id,transaction_time=transaction_time)


def getOrder(userInfo:UserInfo, orderNumber:str):
    sql = "SELECT booking.*, orders.*, \
         attraction.id as a_id, attraction.name as a_name, attraction.address as a_address, attraction.images as a_images \
         FROM orders \
         INNER JOIN booking ON booking.id = orders.booking_id \
         INNER JOIN attraction ON booking.attraction_id = attraction.id \
         WHERE orders.order_number = %s AND booking.user_id = %s"
    val = (orderNumber,userInfo.data.id)
    result = queryDB(sql,val)
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


######################################################################################
######################################################################################
# 取得 attractions 資料列表
app.include_router(getAttractions.router)


# 根據 id 取得 attraction 資料
app.include_router(getAttractionById.router)


# 取得所有捷運站名稱列表，按照週邊景點的數量由大到小排序
app.include_router(getMrts.router)


# 取得當前登入的會員資訊
app.include_router(getUserAuth.router)


# 登入會員帳戶
app.include_router(putUserAuth.router)


# 註冊會員帳戶
app.include_router(postUser.router)


# 建立新的預定行程
app.include_router(postBooking.router)


# 取得尚未確認下單的預訂行程
app.include_router(getBooking.router)


# 刪除目前的預定行程
@app.delete(path="/api/booking")
async def delete_api_booking(request: Request, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    try:
        userInfo = validateJWT(credentials.credentials)
        if isLogin(userInfo):
            result = deleteBooking(userInfo)
            return result
        else:
            return JSONResponse(status_code=403, content=Error(error=True, message="尚未登入").model_dump())
    except:
        return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤").model_dump())


@app.post(path="/api/orders")
async def post_api_orders(request: Request, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], orderInput: OrderInput):
    try:
        userInfo = validateJWT(credentials.credentials)
        if isLogin(userInfo):
            result = registerOrder(orderInput,userInfo)
            return result
        else:
            return JSONResponse(status_code=403, content=Error(error=True, message="尚未登入").model_dump())
    except:
        return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤").model_dump())


@app.get(path="/api/order/{orderNumber}")
async def get_api_order(request: Request, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], orderNumber: str):
    try:
        userInfo = validateJWT(credentials.credentials)
        if isLogin(userInfo):
            result = getOrder(userInfo,orderNumber)
            return result
        else:
            return JSONResponse(status_code=403, content=Error(error=True, message="尚未登入").model_dump())
    except:
        return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤").model_dump())


# Validation Exception Handling
app.add_exception_handler(validationExceptionHandler.CustomValidationException,validationExceptionHandler.custom_validation_exception_handler)

# Http Exception Handling
app.add_exception_handler(httpExceptionHandler.CustomHttpException,httpExceptionHandler.custom_http_exception_handler)

# Static Pages (Never Modify Code in this Block)
app.include_router(staticPage.router)