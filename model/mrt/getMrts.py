from model.DataListModel import DataList

# 捷運站按照景點數量排序
# 輸出
# DataList       資料
def get_mrts(myDB):
    sql = "SELECT mrt.name, count(attraction_mrt.mrt_id) as times \
           FROM attraction_mrt INNER JOIN mrt ON mrt.id = attraction_mrt.mrt_id \
           GROUP BY attraction_mrt.mrt_id ORDER BY times DESC"
    results = myDB.query(sql)
    result = []
    for eachDict in results:
        result.append(eachDict["name"])
    return DataList(data=result)