from pydantic import BaseModel, Field

class UserRead(BaseModel):
    id: int
    username: str = Field(max_length=100)

class UserReadList(BaseModel):
    users: list[UserRead]

class UserCreate(BaseModel):
    username: str = Field(max_length=100)
    password: str = Field(min_length=8, max_length=30)

class UserCreatedReponse(BaseModel):
    id: int

class UserUpdate(UserRead):
    pass

class User(UserRead, UserCreate):
    pass


