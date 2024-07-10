from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated
from model.user.isLogin import isLogin
from model.booking.deleteBooking import deleteBooking
from model.ResponseModel import Error

router = APIRouter()

security = HTTPBearer()

# 刪除目前的預定行程
@router.delete(path="/api/booking")
async def delete_api_booking(request: Request, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    my_jwt = request.app.state.jwt
    myDB = request.app.state.db
    try:
        userInfo = my_jwt.validate(credentials.credentials)
        if isLogin(userInfo):
            result = deleteBooking(myDB, userInfo)
            return result
        else:
            return JSONResponse(status_code=403, content=Error(error=True, message="尚未登入").model_dump())
    except:
        return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤").model_dump())