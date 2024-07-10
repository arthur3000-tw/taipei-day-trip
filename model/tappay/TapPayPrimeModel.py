from pydantic import BaseModel
import datetime

class PrimeOutput(BaseModel):
    status: int
    message: str
    rec_trade_id: str | None = None
    transaction_time: datetime.datetime | None = None
