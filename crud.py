from sqlalchemy.orm import Session
import models, schemas

# ID로 사용자 찾기
def get_user_by_id(db: Session, id: str):
    return db.query(models.User).filter(models.User.id == id).first()

# 모든 사용자 찾기
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# 사용자 생성
def create_user(db: Session, user: schemas.UserSchema):
    db_user = models.User(id=user.id, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 비밀번호 일치 확인
def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password

# 데이터 읽기 - 여러 제품 읽어오기
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

# 데이터 읽기 - ID로 제품 불러오기
def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id
).first()

# 데이터 생성하기 - 제품
def create_item(db: Session, item: schemas.ItemSchema):
    db_item = models.Item(name=item.name, image=item.image, description=item.description, price=item.price, category_id=item.category_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 데이터 읽기 - 제품 카테고리별로 읽어오기
def get_items_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Item).filter(models.Item.categories.any(models.Category.id == category_id)).offset(skip).limit(limit).all()

# 카테고리 생성
def create_item_category(db: Session, category: schemas.CategorySchema):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# 데이터 삭제하기 - 제품 카테고리
def delete_item_category(db: Session, item_id: int, category_id: int):
    Item = db.query(models.Item).filter(models.Item.id == item_id).first()
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    Item.categories.remove(category)
    db.commit()
    db.refresh(Item)
    return Item


def get_reviews(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Review).offset(skip).limit(limit).all()

def get_review(db: Session, review_id: int):
    return db.query(models.Review).filter(models.Review.id == review_id).first()

# 리뷰 생성
def create_review(db: Session, review: schemas.ReviewSchema):
    db_review = models.Review(user_id=review.user_id, item_id=review.item_id, content=review.content, star=review.star)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review