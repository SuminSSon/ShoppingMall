from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 회원가입
@app.post("/join/", response_model=schemas.UserSchema)
def create_user(user: schemas.UserSchema, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User with this ID already registered")
    return crud.create_user(db=db, user=user)

# 로그인
@app.post("/login")
def login(user: schemas.UserSchema, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user or not crud.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return True

# 모든 사용자 보기
@app.get("/users/", response_model=List[schemas.UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
    
# 상품 등록
@app.post("/items/", response_model=schemas.ItemSchema)
def create_item(item: schemas.ItemSchema, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)

# 모든 상품 목록 조회
@app.get("/items/", response_model=List[schemas.ItemSchema])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

# 카테고리 별 상품 목록 조회
@app.get("/items/category/{category_id}", response_model=List[schemas.ItemSchema])
def get_items_by_category(category_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items_by_category(db, category_id=category_id, skip=skip, limit=limit)
    return items

# 제품 명 검색
@app.get("/items/search/{item_name}", response_model=List[schemas.ItemSchema])
def search_items_by_name(item_name: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.search_items_by_name(db, name=item_name, skip=skip, limit=limit)
    return items

# 상품 상세 보기
@app.get("/items/{item_id}", response_model=schemas.ItemSchema)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="item not found")
    return item

# 카테고리 생성
@app.post("/categorys", response_model=schemas.CategorySchema)
def create_item_category(category: schemas.CategorySchema, db: Session = Depends(get_db)):
    return crud.create_item_category(db=db, category=category)

# 리뷰 불러오기
@app.get("/reviews/", response_model=List[schemas.ReviewSchema])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = crud.get_reviews(db, skip=skip, limit=limit)
    return reviews

# 리뷰 생성
@app.post("/items/{item_id}/reviews/", response_model=schemas.ReviewSchema)
def create_review_for_item(item_id: int, review: schemas.ReviewSchema, db: Session = Depends(get_db)):
    return crud.create_review(db=db, review=review)

# 주문하기
@app.post("/order/", response_model=schemas.OrderSchema)
def create_order(order: schemas.OrderSchema, db: Session = Depends(get_db)):
    item = crud.get_item_by_id(db, item_id=order.item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    user = crud.get_user_by_id(db, user_id=order.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    item.price = item.price * order.count

    db_order = crud.create_order(db=db, order=order)
    return db_order

# 유저ID로 주문 내역 조회
@app.get("/orders/user/{user_id}", response_model=List[schemas.OrderSchema])
def get_orders_by_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    orders = crud.get_orders_by_user(db, user_id=user_id)
    
    return orders

# 상품ID로 주문 내역 조회
# item.user_id와 조회하는 Id가 다를 경우 접근 불가
@app.get("/orders/items/{item_id}", response_model=List[schemas.OrderSchema])
def get_orders_by_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item_by_id(db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    orders = crud.get_orders_by_item(db, item_id=item_id)
    return orders

# 결제 완료
@app.put("/order/pay/{order_id}", response_model=schemas.OrderSchema)
def update_order_payment(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.update_order_payment(db, order_id=order_id)
    if db_order:
        return db_order
    else:
        raise HTTPException(status_code=404, detail="Order not found")