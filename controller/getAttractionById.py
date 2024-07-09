from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from model.AttractionModel import AttractionID
from model.responseModel import Error
from model.getAttractionById import get_attraction_id

router = APIRouter()

# 根據 id 取得 attraction 資料
@router.get(path="/api/attraction/{attractionId}", responses={400: {"model": Error}})
async def get_api_attraction_id(request: Request, attractionId: int) -> AttractionID:
    myDB = request.app.state.db
    try:
        result = get_attraction_id(myDB, attractionId)
        return result
    except ValueError:
        return JSONResponse(status_code=400, content=Error(error=True, message="未找到此 ID 之景點資料").model_dump())