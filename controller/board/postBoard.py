from fastapi import APIRouter, Request, File, UploadFile, Form

router = APIRouter()

@router.post(path="/api/board")
async def post_api_board(request: Request, content:str = Form(...), file: UploadFile=File(...)):
    print(content)
    print(file)
    return {"data":{"ok":True}}