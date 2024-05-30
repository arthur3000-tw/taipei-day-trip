from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from mysql.connector import pooling
import json


app = FastAPI()


# 資料庫訊息
myDB = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "taipei_day_trip"
}


# 建立連接池
cnxPool = pooling.MySQLConnectionPool(pool_name="myPool", pool_size=5, **myDB)


# 建立 attraction 資料 model
class Attraction(BaseModel):
    id: int
    name: str
    category: str
    description: str
    address: str
    transport: str
    mrt: str | None = None
    lat: float
    lng: float
    images: list


# 建立 attractions 資料 model
class Attractions(BaseModel):
    nextPage: int | None
    data: list[Attraction]


# 建立 attractionId 資料 model
class AttractionID(BaseModel):
    data: Attraction


# 建立 dataList 資料 model
class DataList(BaseModel):
    data: list


# 建立 error 資料 model
class Error(BaseModel):
    error: bool
    message: str


# 向資料庫查詢
# 輸入
# sql: str      資料庫指令
# val: str      查詢內容
# 輸出
# myResult      查詢結果
def queryDB(sql, val=None):
    # 從連接池取得連線
    cnx = cnxPool.get_connection()
    # 進行操作
    myCursor = cnx.cursor(dictionary=True)
    myCursor.execute(sql, val)
    myResult = myCursor.fetchall()
    # 關閉游標與連接
    myCursor.close()
    cnx.close()
    # 回傳結果
    return myResult


# 以 keyword 查詢
# 輸入
# page: int       頁數
# keyword: str    關鍵字
# 輸出
# Attractions     資料
def attractions(page, keyword=None):
    # 每頁數據量
    pageCounts = 12
    # 未設條件下的查詢語句
    sql = "SELECT attraction.*, mrt.name AS mrt, category.name AS category FROM attraction \
       LEFT JOIN attraction_mrt ON attraction.id = attraction_mrt.attraction_id \
       LEFT JOIN mrt ON mrt.id = attraction_mrt.mrt_id \
       LEFT JOIN attraction_category ON attraction.id = attraction_category.attraction_id \
       LEFT JOIN category ON category.id = attraction_category.category_id "
    if keyword == None:
        result = queryDB(sql,)
    # 加入條件下的查詢
    else:
        sql += "WHERE mrt.name = %s OR attraction.name LIKE %s"
        val = (keyword, "%"+keyword+"%")
        result = queryDB(sql, val)
    # 確認資料數量
    dataCounts = len(result)
    if dataCounts == 0:
        raise ValueError()
    # 計算最大頁數
    maxPage = dataCounts//pageCounts
    # 輸入頁數大於最大頁數或小於0
    if page > maxPage or page < 0:
        raise ValueError()
    else:
        data = []
        # 輸入頁數等於最大頁數
        if page == maxPage:
            for i in range(dataCounts % pageCounts):
                images = json.loads(result[i+page*pageCounts]["images"])
                result[i+page*pageCounts]["images"] = images["images"]
                data.append(Attraction.model_validate(
                    result[i+page*pageCounts]))
            return Attractions(nextPage=None, data=data)
        # 輸入頁數等於 0 小於最大頁數
        else:
            for i in range(12):
                images = json.loads(result[i+page*pageCounts]["images"])
                result[i+page*pageCounts]["images"] = images["images"]
                data.append(Attraction.model_validate(
                    result[i+page*pageCounts]))
            return Attractions(nextPage=page+1, data=data)


# 以 attraction id 查詢
# 輸入
# id: int        id
# 輸出
# Attraction     資料
def attraction_id(id):
    sql = "SELECT attraction.*, mrt.name AS mrt, category.name AS category FROM attraction \
           LEFT JOIN attraction_mrt ON attraction.id = attraction_mrt.attraction_id \
           LEFT JOIN mrt ON mrt.id = attraction_mrt.mrt_id \
           LEFT JOIN attraction_category ON attraction.id = attraction_category.attraction_id \
           LEFT JOIN category ON category.id = attraction_category.category_id \
           WHERE attraction.id = %s"
    val = (id,)
    # 資料庫查詢
    result = queryDB(sql, val)
    if len(result) == 1:
        images = json.loads(result[0]["images"])
        result[0]["images"] = images["images"]
        return AttractionID(data=Attraction.model_validate(result[0]))
    else:
        raise ValueError()


# 捷運站按照景點數量排序
# 輸出
# DataList       資料
def mrts():
    sql = "SELECT mrt.name, count(attraction_mrt.mrt_id) as times \
           FROM attraction_mrt INNER JOIN mrt ON mrt.id = attraction_mrt.mrt_id \
           GROUP BY attraction_mrt.mrt_id ORDER BY times DESC"
    results = queryDB(sql)
    result = []
    for eachDict in results:
        result.append(eachDict["name"])
    return DataList(data=result)


# 取得 attractions 資料列表
@app.get(path="/api/attractions")
async def api_attractions(request: Request, page: int = 0, keyword: str = None) -> Attractions:
    try:
        result = attractions(page, keyword)
        return result
    except ValueError:
        return JSONResponse(status_code=400, content=Error(error=True, message="沒有符合的資料").model_dump())


# 根據 id 取得 attraction 資料
@app.get(path="/api/attraction/{attractionId}", responses={400: {"model": Error}})
async def api_attraction_id(request: Request, attractionId: int) -> AttractionID:
    try:
        result = attraction_id(attractionId)
        return result
    except ValueError:
        return JSONResponse(status_code=400, content=Error(error=True, message="未找到此 ID 之景點資料").model_dump())


# 取得所有捷運站名稱列表，按照週邊景點的數量由大到小排序
@app.get(path="/api/mrts")
async def api_mrts(request: Request) -> DataList:
    result = mrts()
    return result


# Error handling
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=500, content=Error(error=True, message="伺服器內部錯誤").model_dump())


# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
    return FileResponse("./static/index.html", media_type="text/html")


@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
    return FileResponse("./static/attraction.html", media_type="text/html")


@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
    return FileResponse("./static/booking.html", media_type="text/html")


@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
    return FileResponse("./static/thankyou.html", media_type="text/html")
