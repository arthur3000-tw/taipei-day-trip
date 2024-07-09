from fastapi import APIRouter, Request, Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from typing import Annotated
from model.responseModel import Error

router = APIRouter(dependencies=[Depends(security)])

# 取得當前登入的會員資訊
@router.get(path="/api/user/auth")
async def get_api_user_auth(request: Request, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> UserInfo:
    try:
        userInfo = validateJWT(credentials.credentials)
        if isLogin(userInfo):
            return userInfo
        else:
            return JSONResponse(status_code=403, content=userInfo.model_dump())
    except:
        return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤").model_dump())