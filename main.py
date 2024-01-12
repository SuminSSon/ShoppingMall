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
@app.post("/users/", response_model=schemas.UserSchema)
def create_user(user: schemas.UserSchema, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, id=user.id)
    if db_user:
        raise HTTPException(status_code=400, detail="User with this ID already registered")
    return crud.create_user(db=db, user=user)

# 로그인
@app.post("/login")
def login(user: schemas.UserSchema, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, id=user.id)
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


@app.get("/reviews/{review_id}", response_model=schemas.ReviewSchema)
def read_review(review_id: int, db: Session = Depends(get_db)):
    review = crud.get_review(db, review_id=review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

# 리뷰 생성
@app.post("/items/{item_id}/reviews/", response_model=schemas.ReviewSchema)
def create_review_for_item(item_id: int, review: schemas.ReviewSchema, db: Session = Depends(get_db)):
    return crud.create_review(db=db, review=review)
