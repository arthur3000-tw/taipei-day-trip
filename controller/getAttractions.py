from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
from model.AttractionModel import Attractions
from model.responseModel import Error
from model.getAttractions import get_attractions

router = APIRouter()

# 取得 attractions 資料列表
@router.get(path="/api/attractions")
async def get_api_attractions(request: Request, page: int = Query(default=0, ge=0), keyword: str = None) -> Attractions:
    myDB = request.app.state.db
    try:
        result = get_attractions(myDB,page, keyword)
        return result
    except ValueError:
        return JSONResponse(status_code=400, content=Error(error=True, message="沒有符合的資料").model_dump())