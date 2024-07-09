from model.AttractionModel import AttractionID,Attraction
import json

# 以 attraction id 查詢
# 輸入
# id: int        id
# 輸出
# Attraction     資料
def get_attraction_id(myDB,id):
    sql = "SELECT attraction.*, GROUP_CONCAT(DISTINCT mrt.name) AS mrt, GROUP_CONCAT(DISTINCT category.name) AS category \
           FROM attraction \
           LEFT JOIN attraction_mrt ON attraction.id = attraction_mrt.attraction_id \
           LEFT JOIN mrt ON mrt.id = attraction_mrt.mrt_id \
           LEFT JOIN attraction_category ON attraction.id = attraction_category.attraction_id \
           LEFT JOIN category ON category.id = attraction_category.category_id \
           WHERE attraction.id = %s GROUP BY attraction.name"
    val = (id,)
    # 資料庫查詢
    result = myDB.query(sql, val)
    if len(result) == 1:
        images = json.loads(result[0]["images"])
        result[0]["images"] = images["images"]
        return AttractionID(data=Attraction.model_validate(result[0]))
    else:
        raise ValueError()