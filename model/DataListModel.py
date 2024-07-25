from pydantic import BaseModel

# 建立 dataList 資料 model
class DataList(BaseModel):
    data: list