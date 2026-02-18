from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str

class UserOut(BaseModel):
    username: str
    api_key: str