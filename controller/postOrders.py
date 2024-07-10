from fastapi import APIRouter, Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from typing import Annotated
from model.isLogin import isLogin
from model.ResponseModel import Error

router = APIRouter()

security = HTTPBearer()

# 建立新的訂單，並完成付款程序
@router.post(path="/api/orders")
async def post_api_orders(request: Request, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], orderInput: OrderInput):
    my_jwt = request.app.state.jwt
    try:
        userInfo = my_jwt.validate(credentials.credentials)
        if isLogin(userInfo):
            result = registerOrder(orderInput,userInfo)
            return result
        else:
            return JSONResponse(status_code=403, content=Error(error=True, message="尚未登入").model_dump())
    except:
        return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤").model_dump())
