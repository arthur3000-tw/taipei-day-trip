import json
from model.attraction.AttractionModel import Attractions, Attraction


# 以 keyword 查詢
# 輸入
# myDB: object    db物件
# page: int       頁數
# keyword: str    關鍵字
# 輸出
# Attractions     資料
def get_attractions(myDB, page, keyword=None):
    # 每頁數據量
    pageCounts = 12
    # 查詢數量
    queryCounts = pageCounts + 1
    # 計算 offset
    offset = pageCounts * page
    # 未設條件下的查詢語句
    sql = "SELECT attraction.*, GROUP_CONCAT(DISTINCT mrt.name) AS mrt, GROUP_CONCAT(DISTINCT category.name) AS category \
           FROM attraction \
           LEFT JOIN attraction_mrt ON attraction.id = attraction_mrt.attraction_id \
           LEFT JOIN mrt ON mrt.id = attraction_mrt.mrt_id \
           LEFT JOIN attraction_category ON attraction.id = attraction_category.attraction_id \
           LEFT JOIN category ON category.id = attraction_category.category_id "
    # 未設條件狀況下
    if keyword == None:
        # 向資料庫取得資料
        sql += "GROUP BY attraction.id LIMIT %s OFFSET %s"
        val = (queryCounts, offset)
        result = myDB.query(sql, val)
        # 結果數量
        dataCounts = len(result)
        # dataCounts 數量為零（查無結果）
        if dataCounts == 0:
            raise ValueError()
        # 輸出資料
        data = []
        # dataCounts 數量等於 queryCounts 表示有下一頁
        if dataCounts == queryCounts:
            for i in range(pageCounts):
                images = json.loads(result[i]["images"])
                result[i]["images"] = images["images"]
                data.append(Attraction.model_validate(
                    result[i]))
            return Attractions(nextPage=page+1, data=data)
        # result 數量不等於 queryCounts 表示沒有下一頁
        else:
            for i in range(dataCounts):
                images = json.loads(result[i]["images"])
                result[i]["images"] = images["images"]
                data.append(Attraction.model_validate(
                    result[i]))
            return Attractions(nextPage=None, data=data)
    # 加入條件下的查詢
    else:
        # 向資料庫取得資料
        sql += "WHERE mrt.name = %s OR attraction.name LIKE %s \
                GROUP BY attraction.id LIMIT %s OFFSET %s"
        val = (keyword, "%"+keyword+"%", queryCounts, offset)
        result = myDB.query(sql, val)
        # 結果數量
        dataCounts = len(result)
        # dataCounts 數量為零（查無結果）
        if dataCounts == 0:
            raise ValueError()
        # 輸出資料
        data = []
        # dataCounts 數量等於 queryCounts 表示有下一頁
        if dataCounts == queryCounts:
            for i in range(pageCounts):
                images = json.loads(result[i]["images"])
                result[i]["images"] = images["images"]
                data.append(Attraction.model_validate(
                    result[i]))
            return Attractions(nextPage=page+1, data=data)
        # result 數量不等於 queryCounts 表示沒有下一頁
        else:
            for i in range(dataCounts):
                images = json.loads(result[i]["images"])
                result[i]["images"] = images["images"]
                data.append(Attraction.model_validate(
                    result[i]))
            return Attractions(nextPage=None, data=data)