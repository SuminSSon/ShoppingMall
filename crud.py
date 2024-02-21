from sqlalchemy.orm import Session
import models, schemas

# ID로 사용자 찾기
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# 모든 사용자 찾기
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# 사용자 생성
def create_user(db: Session, user: schemas.UserSchema):
    db_user = models.User(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 비밀번호 일치 확인
def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password

# 모든 제품 목록 불러오기
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_item_by_id(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

# ID로 제품 불러오기 (상세 보기)
def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

# 제품 생성
def create_item(db: Session, item: schemas.ItemSchema):
    db_item = models.Item(name=item.name, image=item.image, description=item.description, price=item.price, category_id=item.category_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 카테고리 별 제품 목록
def get_items_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Item).filter(models.Item.category_id == category_id).offset(skip).limit(limit).all()

# 카테고리 생성
def create_item_category(db: Session, category: schemas.CategorySchema):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def search_items_by_name(db: Session, name: str, skip: int = 0, limit: int = 100):
    return db.query(models.Item).filter(models.Item.name.ilike(f"%{name}%")).offset(skip).limit(limit).all()

# 데이터 삭제하기 - 제품 카테고리
def delete_item_category(db: Session, item_id: int, category_id: int):
    Item = db.query(models.Item).filter(models.Item.id == item_id).first()
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    Item.categories.remove(category)
    db.commit()
    db.refresh(Item)
    return Item

# 리뷰 조회
def get_reviews(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Review).offset(skip).limit(limit).all()

# 리뷰 생성
def create_review(db: Session, review: schemas.ReviewSchema):
    db_review = models.Review(user_id=review.user_id, item_id=review.item_id, content=review.content, star=review.star)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# 제품별 리뷰 불러오기
def get_item_reviews(db: Session, item_id: int):
    return db.query(models.Review).filter(models.Review.item_id == item_id).all()

# 주문 생성
def create_order(db: Session, order: schemas.OrderSchema):
    db_order = models.Order(user_id=order.user_id, item_id=order.item_id, price=order.price, count=order.count, pay=order.pay)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders_by_user(db: Session, user_id: int):
    return db.query(models.Order).filter(models.Order.user_id == user_id).all()

def get_orders_by_item(db: Session, item_id: int):
    return db.query(models.Order).filter(models.Order.item_id == item_id).all()

def update_order_payment(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db_order.pay = True
        db.commit()
        db.refresh(db_order)
        return db_order
    return None