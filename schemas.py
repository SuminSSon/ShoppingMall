from typing import Optional, List
from pydantic import BaseModel


class UserSchema(BaseModel):
    id: Optional[int] = None
    email: str
    password: str


class ItemSchema(BaseModel):
    id: Optional[int] = None
    name: str
    image: str
    description: str
    price: int
    category_id: int

class OrderSchema(BaseModel):
    id: Optional[int] = None
    user_id: int
    item_id: int
    price: int
    count: int
    pay: bool

class CategorySchema(BaseModel):
    id: Optional[int] = None
    name: str

class ReviewSchema(BaseModel):
    id: Optional[int] = None
    content: str
    star: int
    user_id: int
    item_id: int