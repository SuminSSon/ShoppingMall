from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(255), primary_key=True, nullable=False)
    password = Column(String(255), nullable=True)

    orders = relationship("Order", backref="user")
    reviews = relationship("Review", backref="user")


class Item(Base):  # 클래스 이름은 Python의 naming convention에 맞게 변경하였습니다.
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    image = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    price = Column(Integer, nullable=True)

    category_id = Column(Integer, ForeignKey("categories.id"))  # 카테고리와의 관계 설정
    category = relationship("Category", backref="items")

    orders = relationship("Order", backref="item")
    reviews = relationship("Review", backref="item")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    price = Column(Integer, nullable=True)
    count = Column(Integer, nullable=True)
    pay = Column(Boolean, default=False, nullable=True)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=True)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(String(255), nullable=True)
    star = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
