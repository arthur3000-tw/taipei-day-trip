from fastapi import APIRouter, Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from typing import Annotated
from model.user.isLogin import isLogin
from model.order.getOrder import getOrder
from model.ResponseModel import Error

router = APIRouter()

security = HTTPBearer()

# 根據訂單編號取得訂單資訊
@router.get(path="/api/order/{orderNumber}")
async def get_api_order(request: Request, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], orderNumber: str):
    my_jwt = request.app.state.jwt
    myDB = request.app.state.db
    try:
        userInfo = my_jwt.validate(credentials.credentials)
        if isLogin(userInfo):
            result = getOrder(myDB,userInfo,orderNumber)
            return result
        else:
            return JSONResponse(status_code=403, content=Error(error=True, message="尚未登入").model_dump())
    except:
        return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤").model_dump())