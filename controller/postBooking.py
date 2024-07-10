from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated
from model.isLogin import isLogin
from model.ResponseModel import OK, Error

router = APIRouter()

security = HTTPBearer()

# 建立新的預定行程
@router.post(path="/api/booking")
async def post_api_booking(request: Request, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], bookingInput: BookingInput) -> OK:
    my_jwt = router.app.state.jwt
    try:
        userInfo = my_jwt.validate(credentials.credentials)
        if isLogin(userInfo):
            result = registerBooking(bookingInput, userInfo)
            return result
        else:
            return JSONResponse(status_code=403, content=Error(error=True, message="尚未登入").model_dump())
    except:
        return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤").model_dump())