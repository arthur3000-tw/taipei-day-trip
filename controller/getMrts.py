from fastapi import APIRouter,Request

router = APIRouter()

# 取得所有捷運站名稱列表，按照週邊景點的數量由大到小排序
@router.get(path="/api/mrts")
async def get_api_mrts(request: Request) -> DataList:
    result = get_mrts()
    return result