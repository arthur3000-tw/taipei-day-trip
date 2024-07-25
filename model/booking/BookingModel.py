from pydantic import BaseModel
import datetime
from model.EnumModel import TimeEnum, PriceEnum


# 建立 attraction info for booking 資料 model
class BookingAttraction(BaseModel):
    id: int
    name: str
    address: str
    image: str


# 建立 booking 資料 model
class Booking(BaseModel):
    attraction: BookingAttraction
    date: datetime.date
    time: str
    price: int


# 建立 booking output 資料 model
class BookingOutput(BaseModel):
    data: Booking | None = None

    
# 建立 booking input 資料 model
class BookingInput(BaseModel):
    attractionId: int
    date: datetime.date
    time: TimeEnum
    price: PriceEnum