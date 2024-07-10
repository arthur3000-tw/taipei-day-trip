from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from model.ResponseModel import Error, OK
from model.signUp import SignUpInfo, signUp

router = APIRouter()

# 註冊會員帳戶
@router.post(path="/api/user", responses={400: {"model": Error}})
async def post_api_user(request: Request, signUpInfo: SignUpInfo) -> OK:
    myDB = request.app.state.db
    try:
        return signUp(myDB, signUpInfo)
    except ValueError:
        return JSONResponse(status_code=400, content=Error(error=True, message="重複的 email").model_dump())