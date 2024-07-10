from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from model.ResponseModel import Error
from model.UserModel import UserAuth
from model.MyJWT import JWT

router = APIRouter()

# 登入會員帳戶
@router.put(path="/api/user/auth", responses={400: {"model": Error}})
async def put_api_user_auth(request: Request, userAuth: UserAuth) -> JWT:
    try:
        result = validateUser(userAuth)
        return result
    except ValueError:
        return JSONResponse(status_code=400, content=Error(error=True, message="未找到此 email 或密碼錯誤").model_dump())