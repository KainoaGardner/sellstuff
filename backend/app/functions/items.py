from sqlalchemy.orm import Session
from app.functions import users
from app.database import models, schemas
from app.password import verify_password, get_password_hash


def get_all_items(db: Session, user_id: int):
    db_user = users.get_user(db, user_id)
    return db_user.items


def get_item(db: Session, user_id: int, item_id: int):
    db_item = (
        db.query(models.Items)
        .filter(models.Items.user_id == user_id, models.Items.id == item_id)
        .first()
    )
    return db_item


def put_new_item(db: Session, user: schemas.User, item: schemas.ItemBase):
    item = models.Items(
        title=item.title,
        description=item.description,
        price=item.price,
        image="",
        sold=item.sold,
        user_id=user.id,
    )
    db.add(item)
    db.commit()
    return item


def toggle_sold(db: Session, db_item: schemas.Item):
    db_item.sold = not db_item.sold
    db.commit()
    return db_item


def update_item(db: Session, db_item: schemas.Item, new_item: schemas.Item):
    if new_item.title:
        db_item.title = new_item.title
    if new_item.description:
        db_item.description = new_item.description
    if new_item.price:
        db_item.price = new_item.price
    if new_item.image:
        db_item.image = new_item.image
    if new_item.sold:
        db_item.sold = new_item.sold
    db.commit()
    return db_item


def delete_item(db: Session, item: schemas.Item):
    db.delete(item)
    db.commit()
    return item
