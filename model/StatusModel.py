from pydantic import BaseModel

class Status(BaseModel):
    status_code: int
    data: int | None = None