from pydantic import BaseModel, EmailStr
import datetime
from model.BookingModel import BookingAttraction
from model.EnumModel import TimeEnum, PriceEnum

class Trip(BaseModel):
    attraction: BookingAttraction
    date: datetime.date
    time: TimeEnum


class Contact(BaseModel):
    name: str
    email: EmailStr
    phone: str


class Order(BaseModel):
    price: PriceEnum
    trip: Trip
    contact: Contact


class OrderInput(BaseModel):
    prime: str
    order: Order


class Payment(BaseModel):
    status: int
    message: str


class OrderInfo(BaseModel):
    number: str
    payment: Payment


class OrderOutput(BaseModel):
    data: OrderInfo


class GetOrder(BaseModel):
    number: str
    price: PriceEnum
    trip: Trip
    contact: Contact
    status: int


class GetOrderOutput(BaseModel):
    data: GetOrder