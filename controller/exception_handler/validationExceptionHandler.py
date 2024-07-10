from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from model.ResponseModel import Error

class CustomValidationException(RequestValidationError):
    pass

async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content=Error(error=True, message="輸入資料型態驗證錯誤").model_dump())
