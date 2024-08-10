import datetime
from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal


class ItemBase(BaseModel):
    title: str
    description: str | None = None
    price: Optional[Decimal] = Field(ge=0.00, decimal_places=2)
    sold: datetime.date | None = None


class ItemChange(BaseModel):
    title: str | None = None
    description: str | None = None
    price: Optional[Decimal] = Field(ge=0.00, decimal_places=2)
    sold: datetime.date | None = None


class Item(ItemBase):
    id: int
    image: str | None = None
    sold: datetime.date | None = None
    user_id: int


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int


class Data(BaseModel):
    total_items: int
    total_sales: int
    average_sale_price: Decimal = Field(ge=0.00, decimal_places=2)
    profit: Decimal = Field(ge=0.00, decimal_places=2)
    biggest_profit_item: str | None = ""


class Token(BaseModel):
    access_token: str
    token_type: str
    id: int
