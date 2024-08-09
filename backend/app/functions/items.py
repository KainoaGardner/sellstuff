from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from app.functions import users
from app.database import models, schemas
from app.password import verify_password, get_password_hash
from datetime import date


def get_all_items(db: Session, user_id: int, sort: str, reverse: bool):
    if sort == "title":
        sort_type = models.Items.title
    elif sort == "price":
        sort_type = models.Items.price
    elif sort == "sold_date":
        sort_type = models.Items.sold
    else:
        sort_type = models.Items.id

    if reverse:
        user_items = (
            db.query(models.Items)
            .filter(models.Items.user_id == user_id)
            .order_by(sort_type.desc())
            .all()
        )
    else:
        user_items = (
            db.query(models.Items)
            .filter(models.Items.user_id == user_id)
            .order_by(sort_type)
            .all()
        )

    return user_items


def get_item(db: Session, item_id: int):
    db_item = db.query(models.Items).filter(models.Items.id == item_id).first()
    return db_item


# def get_image_path(db: Session, item_id: int):
#     db_item = db.query(models.Items).filter(models.Items.id == item_id).first()
#     return db_item.image
#


def put_new_item(db: Session, user_id: int, item: schemas.ItemBase):
    item = models.Items(
        title=item.title,
        description=item.description,
        price=item.price * 100,
        # image="",
        sold=item.sold,
        user_id=user_id,
    )
    db.add(item)
    db.commit()
    return item


def put_image(db: Session, db_item: schemas.Item, path: str):
    db_item.image = path
    db.commit()


def toggle_sold(db: Session, db_item: schemas.Item):
    if db_item.sold:
        db_item.sold = None
    else:
        db_item.sold = date.today()

    db.commit()
    return db_item


def update_item(db: Session, db_item: schemas.Item, new_item: schemas.Item):
    if new_item.title:
        db_item.title = new_item.title
    if new_item.description:
        db_item.description = new_item.description
    if new_item.price:
        db_item.price = new_item.price * 100
    # if new_item.image:
    #     db_item.image = new_item.image
    if new_item.sold:
        db_item.sold = new_item.sold
    db.commit()
    return db_item


def delete_item(db: Session, item: schemas.Item):
    db.delete(item)
    db.commit()
    return item
