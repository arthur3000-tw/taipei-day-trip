from controller.mrt import getMrts
from controller import staticPage
from controller.attraction import getAttractionById, getAttractions
from controller.booking import deleteBooking, getBooking, postBooking
from controller.exception_handler import httpExceptionHandler, validationExceptionHandler
from controller.order import getOrder, postOrders
from controller.user import getUserAuth, postUser, putUserAuth
from controller.board import postBoard, getBoard
from model.jwt import MyJWT
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from model.db import DB

# app 加入 dependencies
app = FastAPI()
app.mount('/static', StaticFiles(directory='static', html=True))

# DB 實體化
myDB = DB.DB(host="db-mysql-1.cvssiko2are2.ap-southeast-1.rds.amazonaws.com",database="taipei_day_trip")
myDB.initialize()
# db instance 存放於 app.state 中
app.state.db = myDB

# 實體化 MyJWT
# 設定 expired days = 7, algorithm = HS256
my_jwt = MyJWT.MyJWT(jwt_secret_key = os.environ.get("JWT_SECRET_KEY"), expired_days = 7, jwt_algorithm = "HS256")
# MyJWT instance 存放於 app.state 中
app.state.jwt = my_jwt

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
app.include_router(deleteBooking.router)

# 建立新的訂單，並完成付款程序
app.include_router(postOrders.router)

# 根據訂單編號取得訂單資訊
app.include_router(getOrder.router)

# Validation Exception Handling
app.add_exception_handler(validationExceptionHandler.CustomValidationException,validationExceptionHandler.custom_validation_exception_handler)

# Http Exception Handling
app.add_exception_handler(httpExceptionHandler.CustomHttpException,httpExceptionHandler.custom_http_exception_handler)

# Static Pages (Never Modify Code in this Block)
app.include_router(staticPage.router)

# 新增圖文留言板
app.include_router(postBoard.router)

# 取得圖文留言板
app.include_router(getBoard.router)