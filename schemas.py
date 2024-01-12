from typing import Optional, List
from pydantic import BaseModel


class UserSchema(BaseModel):
    id: str
    password: str


class ItemSchema(BaseModel):
    name: str
    image: str
    description: str
    price: int
    category_id: int

class OrderSchema(BaseModel):
    user_id: str
    item_id: str
    price: int
    count: int
    pay: bool

class CategorySchema(BaseModel):
    name: str

class ReviewSchema(BaseModel):
    content: str
    star: int
    user_id: int
    item_id: int
