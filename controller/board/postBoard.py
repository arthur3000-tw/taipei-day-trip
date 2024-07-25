from fastapi import APIRouter, Request, File, UploadFile, Form
from fastapi.responses import JSONResponse
from model.board.postBoard import post_board
from model.ResponseModel import Error,OK

router = APIRouter()

@router.post(path="/api/board")
async def post_api_board(request: Request, content:str = Form(...), file: UploadFile=File(...)):
    myDB = request.app.state.db
    try:
        result = post_board(myDB,content,file)
    except:
        return JSONResponse(status_code=400, content=Error(error=True, message="S3 上傳錯誤").model_dump())
    if result.status_code == 1:
        return JSONResponse(status_code=400, content=Error(error=True, message="S3 上傳錯誤").model_dump())
    elif result.status_code ==2:
        return JSONResponse(status_code=400, content=Error(error=True, message="資料庫寫入錯誤").model_dump())
    elif result.status_code == 0:
        return OK(ok=True)
    else:
        return JSONResponse(status_code=400, content=Error(error=True, message="其他錯誤").model_dump())