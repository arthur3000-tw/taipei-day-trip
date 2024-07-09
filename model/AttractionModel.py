from pydantic import BaseModel

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