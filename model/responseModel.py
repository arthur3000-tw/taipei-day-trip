from pydantic import BaseModel

class Error(BaseModel):
    error: bool
    message: str