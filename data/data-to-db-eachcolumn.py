import json
import mysql.connector

# 資料庫資訊
myDB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="taipei_day_trip"
)


# 建立 myCursor 物件
myCursor = myDB.cursor(dictionary=True)


# 開啟文件
with open("taipei-attractions.json", "r") as f:
    # 解析 json
    data = json.load(f)
    data = data["result"]["results"]


# name, description, address, transport, lat, lng 放入資料庫 attraction 表格
for i in data:
    sql = "INSERT INTO attraction (name, description, address, transport, lat, lng) VALUES (%s,%s,%s,%s,%s,%s)"
    val = (i["name"], i["description"], i["address"],
           i["direction"], i["latitude"], i["longitude"])
    myCursor.execute(sql, val)
    myDB.commit()


# mrt 是否存在於資料庫中
def is_MRT_existed(name):
    sql = "SELECT name FROM mrt WHERE name = %s"
    val = (name,)
    myCursor.execute(sql, val)
    myResult = myCursor.fetchall()
    if (len(myResult) == 0):
        return False
    elif (len(myResult) == 1):
        return True


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
        myCursor.execute(sql, val)
        myDB.commit()
    # 取得 attraction id
    sql = "SELECT id FROM attraction WHERE name = %s"
    val = (name,)
    myCursor.execute(sql, val)
    myResult = myCursor.fetchall()
    attraction_id = myResult[0]["id"]
    # 取得 mrt id
    sql = "SELECT id FROM mrt WHERE name = %s"
    val = (mrt,)
    myCursor.execute(sql, val)
    myResult = myCursor.fetchall()
    mrt_id = myResult[0]["id"]
    # 將 relation 加入 attraction_mrt 表格
    sql = "INSERT INTO attraction_mrt (attraction_id,mrt_id) VALUES (%s,%s)"
    val = (attraction_id, mrt_id)
    myCursor.execute(sql, val)
    myDB.commit()


# category 是否存在於資料庫中
def is_category_existed(name):
    sql = "SELECT name FROM category WHERE name = %s"
    val = (name,)
    myCursor.execute(sql, val)
    myResult = myCursor.fetchall()
    if (len(myResult) == 0):
        return False
    elif (len(myResult) == 1):
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
        myCursor.execute(sql, val)
        myDB.commit()
    # 取得 attraction id
    sql = "SELECT id FROM attraction WHERE name = %s"
    val = (name,)
    myCursor.execute(sql, val)
    myResult = myCursor.fetchall()
    attraction_id = myResult[0]["id"]
    # 取得 category id
    sql = "SELECT id FROM category WHERE name = %s"
    val = (category,)
    myCursor.execute(sql, val)
    myResult = myCursor.fetchall()
    category_id = myResult[0]["id"]
    # 將 relation 加入 attraction_category 表格
    sql = "INSERT INTO attraction_category (attraction_id,category_id) VALUES (%s,%s)"
    val = (attraction_id, category_id)
    myCursor.execute(sql, val)
    myDB.commit()


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
    val = (json_dumps_images, name)
    myCursor.execute(sql, val)
    myDB.commit()
