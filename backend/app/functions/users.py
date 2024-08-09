from sqlalchemy.orm import Session
from app.database import models, schemas
from app.functions import items, data
from app.password import verify_password, get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def get_all_users(db: Session) -> list:
    return db.query(models.Users).all()


def get_data(db: Session, user_id: int):
    total_items = data.total_items(db, user_id)
    total_sales = data.total_sales(db, user_id)
    average_sale = data.average_sale(db, user_id)
    profit = data.sale_profit(db, user_id)
    biggest_profit = data.biggest_profit(db, user_id)

    result = {
        "total_items": total_items,
        "total_sales": total_sales,
        "average_sale_price": average_sale,
        "profit": profit,
        "biggest_profit_item": biggest_profit,
    }
    print(result)
    return result


def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
    hashed_password = get_password_hash(user.password)
    db_user = models.Users(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_username(db: Session, username: str) -> schemas.User:
    db_user = db.query(models.Users).filter(models.Users.username == username).first()
    return db_user


def remove_user(db: Session, db_user: schemas.User) -> schemas.User:
    db.delete(db_user)
    db.commit()
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    else:
        return user
