from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from model import responseModel

class CustomValidationException(RequestValidationError):
    pass

async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content=responseModel.Error(error=True, message="輸入資料型態驗證錯誤").model_dump())