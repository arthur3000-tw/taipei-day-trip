from fastapi import APIRouter,Request
from fastapi.responses import JSONResponse
from model.board.getBoard import get_board
from model.ResponseModel import Error, OK

router = APIRouter()

@router.get(path="/api/board")
async def get_api_board(request:Request):
    myDB = request.app.state.db
    try:
        result = get_board(myDB)
        return result
    except:
        return JSONResponse(status_code=400, content=Error(error=True, message="無法取得資料").model_dump())