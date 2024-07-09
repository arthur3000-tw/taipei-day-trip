from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from model import responseModel

router = APIRouter()

# http exception handling
@router.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_403_FORBIDDEN:
        return JSONResponse(status_code=403, content=responseModel.Error(error=True, message="尚未登入").model_dump())