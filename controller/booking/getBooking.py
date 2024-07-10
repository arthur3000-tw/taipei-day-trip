from fastapi import APIRouter, Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from typing import Annotated
from model.user.isLogin import isLogin
from model.booking.getBooking import getBooking
from model.ResponseModel import Error

router = APIRouter()

security = HTTPBearer()

# 取得尚未確認下單的預訂行程
@router.get(path="/api/booking")
async def get_api_booking(request: Request, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    my_jwt = request.app.state.jwt
    myDB = request.app.state.db
    try:
        userInfo = my_jwt.validate(credentials.credentials)
        if isLogin(userInfo):
            result = getBooking(myDB, userInfo)
            return result
        else:
            return JSONResponse(status_code=403, content=Error(error=True, message="尚未登入").model_dump())
    except:
        return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤").model_dump())