import json
import mysql.connector
# from pydantic import BaseModel

# 資料庫資訊
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="taipei_day_trip"
)
mycursor = mydb.cursor(dictionary=True)

# 開啟文件
with open("taipei-attractions.json", "r") as f:
    # 解析 json
    data = json.load(f)
    data = data["result"]["results"]

# print("name: " + data[0]["name"])
# print("description: " + data[0]["description"])
# print("address: " + data[0]["address"])
# print("transport: " + data[0]["direction"])
# print("lat: " + data[0]["latitude"])
# print("lng: " + data[0]["longitude"])

# name, description, address, transport, lat, lng 放入資料庫 attraction 表格
for i in data:
    sql = "INSERT INTO attraction (name, description, address, transport, lat, lng) VALUES (%s,%s,%s,%s,%s,%s)"
    val = (i["name"],i["description"],i["address"],i["direction"],i["latitude"],i["longitude"])
    mycursor.execute(sql,val)
    mydb.commit()

# print("mrt: " + data[0]["MRT"])
# print(data[26]["MRT"] == None)

# mrt = data[0]["MRT"]
# sql = "SELECT id FROM mrt WHERE name = %s"
# val = (mrt,)
# mycursor.execute(sql,val)
# myresult = mycursor.fetchall()
# print(myresult)
# print(myresult[0]["id"])

# mrt 是否存在於資料庫中
def is_MRT_existed(name):
    sql = "SELECT name FROM mrt WHERE name = %s"
    val = (name,)
    mycursor.execute(sql,val)
    myresult = mycursor.fetchall()
    if (len(myresult)==0):
        return False
    elif (len(myresult)==1):
        return True

# print(not is_MRT_existed(mrt))

# mrt 放入資料庫 mrt, attraction_mrt 表格
for i in data:
    # 取得 mrt 站名
    mrt = i["MRT"]
    if mrt == None:
        continue
    # 取得地點名稱
    name = i["name"]
    # 確認 mrt 表格中是否有此 mrt
    if not is_MRT_existed(mrt):
        # 新增 mrt 車站至 mrt 表格
        sql = "INSERT INTO mrt (name) VALUES (%s)"
        val = (mrt,)
        mycursor.execute(sql,val)
        mydb.commit()
    # 取得 attraction id
    sql = "SELECT id FROM attraction WHERE name = %s"
    val = (name,)
    mycursor.execute(sql,val)
    myresult = mycursor.fetchall()
    attraction_id = myresult[0]["id"]
    # 取得 mrt id
    sql = "SELECT id FROM mrt WHERE name = %s"
    val = (mrt,)
    mycursor.execute(sql,val)
    myresult = mycursor.fetchall()
    mrt_id = myresult[0]["id"]
    # 將 relation 加入 attraction_mrt 表格
    sql = "INSERT INTO attraction_mrt (attraction_id,mrt_id) VALUES (%s,%s)"
    val = (attraction_id,mrt_id)
    mycursor.execute(sql,val)
    mydb.commit()

# category 是否存在於資料庫中
def is_category_existed(name):
    sql = "SELECT name FROM category WHERE name = %s"
    val = (name,)
    mycursor.execute(sql,val)
    myresult = mycursor.fetchall()
    if (len(myresult)==0):
        return False
    elif (len(myresult)==1):
        return True

# category 放入資料庫 category, attraction_category 表格
for i in data:
    # 取得 category 名稱
    category = i["CAT"]
    if category == None:
        continue
    # 取得地點名稱
    name = i["name"]
    # 確認 category 表格中是否有此 category
    if not is_category_existed(category):
        # 新增類別至 category 表格
        sql = "INSERT INTO category (name) VALUES (%s)"
        val = (category,)
        mycursor.execute(sql,val)
        mydb.commit()
    # 取得 attraction id
    sql = "SELECT id FROM attraction WHERE name = %s"
    val = (name,)
    mycursor.execute(sql,val)
    myresult = mycursor.fetchall()
    attraction_id = myresult[0]["id"]
    # 取得 category id
    sql = "SELECT id FROM category WHERE name = %s"
    val = (category,)
    mycursor.execute(sql,val)
    myresult = mycursor.fetchall()
    category_id = myresult[0]["id"]
    # 將 relation 加入 attraction_category 表格
    sql = "INSERT INTO attraction_category (attraction_id,category_id) VALUES (%s,%s)"
    val = (attraction_id,category_id)
    mycursor.execute(sql,val)
    mydb.commit()

# print("file: " + data[0]["file"])
# file = data[1]["file"].split("https://")
# print(file[2].endswith(".JPG"))
# images = []
# for i in file:
#     if (i.endswith(".jpg") or i.endswith(".JPG")):
#         i = "https://" + i
#         images.append(i)
# print(images)
# json_images = {"images": images}
# print(json_images)
# json_dumps_images = json.dumps(json_images)
# json_dumps_images = json.dumps({"images": images})
# print(json_dumps_images)

# 將 image 連結放入資料庫中
for i in data:
    # 取得地點名稱
    name = i["name"]
    # 取得連結放入 file
    file = i["file"].split("https://")
    images = []
    # 篩選 .jpg 檔案與 .JPG 檔案
    for j in file:
        if (j.endswith(".jpg") or j.endswith(".JPG")):
            j = "https://" + j
            images.append(j)
    # 轉換為 JSON 格式
    json_dumps_images = json.dumps({"images": images})
    # 放入 images 資料
    sql = "UPDATE attraction SET images = %s WHERE name = %s"
    val = (json_dumps_images,name)
    mycursor.execute(sql,val)
    mydb.commit()


# 建立 attraction 資料 model
# class Attraction(BaseModel):
#     id: int 
#     name: str 
#     category: str 
#     description: str 
#     address: str 
#     transport: str
#     mrt: str| None = None
#     lat: float 
#     lng: float
#     images: list


# id = 60 
# sql = "SELECT * FROM attraction WHERE id = %s"
# sql = "SELECT attraction.*, mrt.name AS mrt, category.name AS category FROM attraction \
#        LEFT JOIN attraction_mrt ON attraction.id = attraction_mrt.attraction_id \
#        LEFT JOIN mrt ON mrt.id = attraction_mrt.mrt_id \
#        LEFT JOIN attraction_category ON attraction.id = attraction_category.attraction_id \
#        LEFT JOIN category ON category.id = attraction_category.category_id \
#        WHERE attraction.id = %s"
# val = (id,)
# mycursor.execute(sql,val)
# myresult = mycursor.fetchall()
# print(myresult[0])
# print(len(myresult))
# print(myresult[0]["images"])
# images = json.loads(myresult[0]["images"])
# print(images["images"])
# myresult[0]["images"] = images["images"]
# data = Attraction.model_validate(myresult[0])

# from mysql.connector import pooling
# myDB = {
#     "host": "localhost",
#     "user": "root",
#     "password": "password",
#     "database": "taipei_day_trip"
# }
# cnxPool = pooling.MySQLConnectionPool(pool_name="myPool", pool_size=5, **myDB)
# def queryDB(sql, val=None):
#     # 從連接池取得連線
#     cnx = cnxPool.get_connection()
#     # 進行操作
#     myCursor = cnx.cursor(dictionary=True)
#     # if val == None:
#     #     myCursor.execute(sql)
#     # else:
#     myCursor.execute(sql, val)
#     myResult = myCursor.fetchall()
#     # 關閉游標與連接
#     myCursor.close()
#     cnx.close()
#     # 回傳結果
#     return myResult


# sql = "SELECT mrt.name, count(attraction_mrt.mrt_id) as times \
#        FROM attraction_mrt INNER JOIN mrt ON mrt.id = attraction_mrt.mrt_id \
#        GROUP BY attraction_mrt.mrt_id ORDER BY times DESC"
# myresult = queryDB(sql)
# myresult = mycursor.fetchall()
# data = []
# for i in myresult:
#     data.append(i["name"])
# print(data)

# 建立 attractions 資料 model
# class Attractions(BaseModel):
#     nextPage: int
#     data: list[Attraction]

# pageCounts = 12
# page = 0
# keyword = None
# sql = "SELECT attraction.*, mrt.name AS mrt, category.name AS category FROM attraction \
#        LEFT JOIN attraction_mrt ON attraction.id = attraction_mrt.attraction_id \
#        LEFT JOIN mrt ON mrt.id = attraction_mrt.mrt_id \
#        LEFT JOIN attraction_category ON attraction.id = attraction_category.attraction_id \
#        LEFT JOIN category ON category.id = attraction_category.category_id \
#        WHERE mrt.name = %s OR attraction.name LIKE %s"
# val = (keyword,"%"+keyword+"%")
# myresult = queryDB(sql,val)
# print(len(myresult))
# dataCounts = len(myresult)
# maxPage = dataCounts//pageCounts
# if page > maxPage or page < 0:
#     print("超出範圍")
# else:
#     data = []
#     if page == maxPage:
#         for i in range(dataCounts%pageCounts):
#             images = json.loads(myresult[i+page*pageCounts]["images"])
#             myresult[i+page*pageCounts]["images"] = images["images"]
#             data.append(Attraction.model_validate(myresult[i+page*pageCounts]))
#     else:
#         for i in range(12):
#             images = json.loads(myresult[i+page*pageCounts]["images"])
#             myresult[i+page*pageCounts]["images"] = images["images"]
#             data.append(Attraction.model_validate(myresult[i+page*pageCounts]))
#     # print(data)
#     output = Attractions(nextPage=page,data=data)

# page = 0
# count = 0
# for dicts in myresult:
#     if count == 11:
#         page += 1
    
#     count +=1