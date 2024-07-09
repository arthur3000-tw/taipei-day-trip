from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
from model.AttractionModel import Attractions
from model.responseModel import Error

router = APIRouter()

# 取得 attractions 資料列表
@router.get(path="/api/attractions")
async def get_api_attractions(request: Request, page: int = Query(default=0, ge=0), keyword: str = None) -> Attractions:
    try:
        result = get_attractions(page, keyword)
        return result
    except ValueError:
        return JSONResponse(status_code=400, content=Error(error=True, message="沒有符合的資料").model_dump())