from controller import staticPage,httpExceptionHandler,validationExceptionHandler,getAttraction
from model import db
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


app = FastAPI()
app.mount('/static', StaticFiles(directory='static', html=True))


security = HTTPBearer()








# 建立 dataList 資料 model
class DataList(BaseModel):
    data: list


# 建立 user 資料 model
class User(BaseModel):
    id: int | None
    name: str | None
    email: EmailStr | None


# 建立 userInfo 資料 model
class UserInfo(BaseModel):
    data: User | None = None


# 建立 signUpInfo 資料 model
class SignUpInfo(BaseModel):
    name: str
    email: EmailStr
    password: str


# 建立 userAuth 資料 model
class UserAuth(BaseModel):
    email: EmailStr
    password: str


# 建立 jwt 資料 model
class JWT(BaseModel):
    token: str


# 建立 attraction info for booking 資料 model
class BookingAttraction(BaseModel):
    id: int
    name: str
    address: str
    image: str


# 建立 booking 資料 model
class Booking(BaseModel):
    attraction: BookingAttraction
    date: datetime.date
    time: str
    price: int


class BookingOutput(BaseModel):
    data: Booking | None = None


class TimeEnum(str, Enum):
    morning = "morning"
    afternoon = "afternoon"


class PriceEnum(IntEnum):
    morning = 2000
    afternoon = 2500


class BookingInput(BaseModel):
    attractionId: int
    date: datetime.date
    time: TimeEnum
    price: PriceEnum


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



class Status(BaseModel):
    status_code: int
    data: int | None = None


# 建立 ok 資料 model
class OK(BaseModel):
    ok: bool


# 建立 error 資料 model
class Error(BaseModel):
    error: bool
    message: str





# 向資料庫輸入資料
def insertDB(sql, val):
    # 從連接池取得連線
    cnx = cnxPool.get_connection()
    # 進行操作
    myCursor = cnx.cursor(dictionary=True)
    myCursor.execute(sql, val)
    cnx.commit()
    myResult = myCursor.rowcount
    # 關閉游標與連接
    myCursor.close()
    cnx.close()
    # 回傳結果
    return myResult





# 以 attraction id 查詢
# 輸入
# id: int        id
# 輸出
# Attraction     資料
def get_attraction_id(id):
    sql = "SELECT attraction.*, GROUP_CONCAT(DISTINCT mrt.name) AS mrt, GROUP_CONCAT(DISTINCT category.name) AS category \
           FROM attraction \
           LEFT JOIN attraction_mrt ON attraction.id = attraction_mrt.attraction_id \
           LEFT JOIN mrt ON mrt.id = attraction_mrt.mrt_id \
           LEFT JOIN attraction_category ON attraction.id = attraction_category.attraction_id \
           LEFT JOIN category ON category.id = attraction_category.category_id \
           WHERE attraction.id = %s GROUP BY attraction.name"
    val = (id,)
    # 資料庫查詢
    result = queryDB(sql, val)
    if len(result) == 1:
        images = json.loads(result[0]["images"])
        result[0]["images"] = images["images"]
        return AttractionID(data=Attraction.model_validate(result[0]))
    else:
        raise ValueError()


# 捷運站按照景點數量排序
# 輸出
# DataList       資料
def get_mrts():
    sql = "SELECT mrt.name, count(attraction_mrt.mrt_id) as times \
           FROM attraction_mrt INNER JOIN mrt ON mrt.id = attraction_mrt.mrt_id \
           GROUP BY attraction_mrt.mrt_id ORDER BY times DESC"
    results = queryDB(sql)
    result = []
    for eachDict in results:
        result.append(eachDict["name"])
    return DataList(data=result)


# 註冊帳號
def signUp(signUpInfo: SignUpInfo):
    # 資料庫查詢是否有此 email
    sql = "SELECT * FROM user WHERE email = %s"
    val = (signUpInfo.email,)
    result = queryDB(sql, val)
    # 無重複 email
    if len(result) == 0:
        # 將密碼加密
        encodedPassword = encodePassword(signUpInfo.password)
        # 輸入資料庫
        sql = "INSERT INTO user (name, email, password) VALUES (%s, %s, %s)"
        val = (signUpInfo.name, signUpInfo.email, encodedPassword)
        result = insertDB(sql, val)
        # 輸入完成
        if result == 1:
            return OK(ok=True)
        # 輸入失敗
        else:
            raise ValueError()
    # 有重複 email
    else:
        raise ValueError()


# 驗證使用者
# 輸入
# userAuth 格式資料
# 輸出
# 密碼正確： JWT 格式資料
# 密碼錯誤： ValueError()
def validateUser(userAuth: UserAuth):
    # 資料庫查詢是否有此 email
    sql = "SELECT * FROM user WHERE email = %s"
    val = (userAuth.email,)
    result = queryDB(sql, val)
    # 有找到此 email 且密碼正確
    if len(result) == 1 and validatePassword(userAuth.password, result[0]["password"]):
        # 進行製作 JWT，設置七天時間期限
        payload = {"id": result[0]["id"], "name": result[0]
                   ["name"], "email": result[0]["email"]}
        return JWT(token=generateJWT(payload, EXPIRED_DAYS))
    # 未找到此 email 或密碼錯誤
    else:
        raise ValueError()


# jwt 加密參數
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
EXPIRED_DAYS = 7
JWT_ALGORITHM = "HS256"


# 製作 JWT
# 輸入
# payload: 加密資料
# days: 有效期限天數
# 輸出
# encoded_jwt: JWT
def generateJWT(payload, days):
    exp = datetime.datetime.now(
        tz=datetime.timezone.utc) + datetime.timedelta(days=days)
    payload["exp"] = exp
    encoded_jwt = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


# 驗證 JWT
# 輸入
# token: JWT
# 輸出
# UserInfo 資料
def validateJWT(token):
    try:
        result = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return UserInfo(data=User(id=result["id"], name=result["name"], email=result["email"]))
    except:
        return UserInfo(User=None)


# 驗證密碼
# 輸入
# userPassword: 使用者輸入密碼
# dbPassword: 資料庫中密碼
# 輸出
# boolean
def validatePassword(userPassword, dbPassword):
    userPassword = userPassword.encode("utf-8")
    dbPassword = dbPassword.encode("utf-8")
    return bcrypt.checkpw(userPassword, dbPassword)


# 密碼加密
# 輸入
# password: 密碼
# 輸出
# hash: 加密密碼
def encodePassword(password):
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash


# 確認登入狀態
# 輸入
# UserInfo
# 輸出
# boolean
def isLogin(user_info):
    if user_info.data == None:
        return False
    else:
        return True


# 確認 booking 資料
# 輸入
# BookingInput
# UserInfo
# 輸出
# boolean
def isBookingRegistered(bookingInput: BookingInput, userInfo: UserInfo):
    userId = userInfo.data.id
    attractionId = bookingInput.attractionId
    date = bookingInput.date
    time = bookingInput.time
    # 向資料庫取得資料
    sql = "SELECT * FROM booking WHERE user_id = %s AND attraction_id = %s AND date = %s AND time = %s AND ordered = %s"
    val = (userId, attractionId, date, time, False)
    result = queryDB(sql, val)
    # 結果數量
    dataCounts = len(result)
    # dataCounts 數量為零（查無結果）
    if dataCounts == 0:
        return False
    else:
        return True


# 更新 booking 資料
# 輸入
# bookingInput
# userInfo
# 輸出 Status 資料
# status_code = 0 => 更新完成
# status_code = 1 => 錯誤
def updateBooking(bookingInput: BookingInput, userInfo: UserInfo):
    userId = userInfo.data.id
    attractionId = bookingInput.attractionId
    date = bookingInput.date
    time = bookingInput.time
    log_time = datetime.datetime.now()
    # 更新資料庫資料
    sql = "UPDATE booking SET log_time = %s \
         WHERE user_id = %s AND attraction_id = %s AND date = %s AND time = %s"
    val = (log_time, userId, attractionId, date, time)
    result = insertDB(sql, val)
    if result == 1:
        return Status(status_code=0)
    else:
        return Status(status_code=1)


# 記錄 booking 狀況
# 輸入
# bookingInput
# userInfo
# 輸出
def registerBooking(bookingInput: BookingInput, userInfo: UserInfo):
    # 確認 booking 狀況
    # 若已經有重複 booking 狀況
    if isBookingRegistered(bookingInput, userInfo):
        result = updateBooking(bookingInput, userInfo)
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
        result = insertDB(sql, val)
        if result == 1:
            return OK(ok=True)
        else:
            return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤").model_dump())


# 取得 booking 資料
# 輸入
# userInfo
# 輸出
# Booking 資料
def getBooking(userInfo: UserInfo):
    # 取出資料
    userId = userInfo.data.id
    # 資料庫指令
    sql = "SELECT * FROM booking WHERE user_id = %s AND ordered = %s ORDER BY log_time DESC LIMIT 1"
    val = (userId,False)
    result = queryDB(sql, val)
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
app.include_router(getAttraction.router)


# 根據 id 取得 attraction 資料
@app.get(path="/api/attraction/{attractionId}", responses={400: {"model": Error}})
async def get_api_attraction_id(request: Request, attractionId: int) -> AttractionID:
    try:
        result = get_attraction_id(attractionId)
        return result
    except ValueError:
        return JSONResponse(status_code=400, content=Error(error=True, message="未找到此 ID 之景點資料").model_dump())


# 取得所有捷運站名稱列表，按照週邊景點的數量由大到小排序
@app.get(path="/api/mrts")
async def get_api_mrts(request: Request) -> DataList:
    result = get_mrts()
    return result


# 取得當前登入的會員資訊
@app.get(path="/api/user/auth")
async def get_api_user_auth(request: Request, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> UserInfo:
    try:
        userInfo = validateJWT(credentials.credentials)
        if isLogin(userInfo):
            return userInfo
        else:
            return JSONResponse(status_code=403, content=userInfo.model_dump())
    except:
        return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤").model_dump())


# 登入會員帳戶
@app.put(path="/api/user/auth", responses={400: {"model": Error}})
async def put_api_user_auth(request: Request, userAuth: UserAuth) -> JWT:
    try:
        result = validateUser(userAuth)
        return result
    except ValueError:
        return JSONResponse(status_code=400, content=Error(error=True, message="未找到此 email 或密碼錯誤").model_dump())


# 註冊會員帳戶
@app.post(path="/api/user", responses={400: {"model": Error}})
async def post_api_user(request: Request, signUpInfo: SignUpInfo) -> OK:
    try:
        return signUp(signUpInfo)
    except ValueError:
        return JSONResponse(status_code=400, content=Error(error=True, message="重複的 email").model_dump())


# 建立新的預定行程
@app.post(path="/api/booking")
async def post_api_booking(request: Request, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], bookingInput: BookingInput) -> OK:
    try:
        userInfo = validateJWT(credentials.credentials)
        if isLogin(userInfo):
            result = registerBooking(bookingInput, userInfo)
            return result
        else:
            return JSONResponse(status_code=403, content=Error(error=True, message="尚未登入").model_dump())
    except:
        return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤").model_dump())


# 取得尚未確認下單的預訂行程
@app.get(path="/api/booking")
async def get_api_booking(request: Request, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    try:
        userInfo = validateJWT(credentials.credentials)
        if isLogin(userInfo):
            result = getBooking(userInfo)
            return result
        else:
            return JSONResponse(status_code=403, content=Error(error=True, message="尚未登入").model_dump())
    except:
        return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤").model_dump())


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