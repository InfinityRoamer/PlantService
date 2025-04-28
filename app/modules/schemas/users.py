from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserToken(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
