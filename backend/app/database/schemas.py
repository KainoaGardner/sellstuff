from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None
    price: float | None = 0
    sold: bool | None = False


class ItemChange(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = 0
    sold: bool | None = False


class Item(ItemBase):
    id: int
    image: str | None = None
    sold: bool | None = False
    user_id: int


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str
