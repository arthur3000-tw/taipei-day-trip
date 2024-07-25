from fastapi import APIRouter, Request, File, UploadFile, Form
from model.board.postBoard import post_board

router = APIRouter()

@router.post(path="/api/board")
async def post_api_board(request: Request, content:str = Form(...), file: UploadFile=File(...)):
    print(content)
    print(file)
    myDB = request.app.state.db
    try:
        result = post_board(myDB,content,file)
    except:
        return {"data":{"error":True}}
    return {"data":{"ok":True}}