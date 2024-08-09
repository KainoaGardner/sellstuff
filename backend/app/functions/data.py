from sqlalchemy import text
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from app.database import models


def total_items(db: Session, user_id: int):
    user_items = db.query(models.Items).filter(models.Items.user_id == user_id).all()
    return len(user_items)


def total_sales(db: Session, user_id: int):
    sold_items = (
        db.query(models.Items)
        .filter(models.Items.user_id == user_id, models.Items.sold != None)
        .all()
    )
    return len(sold_items)


def average_sale(db: Session, user_id: int):
    average = round(
        db.query(func.avg(models.Items.price))
        .filter(models.Items.user_id == user_id, models.Items.sold != None)
        .scalar()
        / 100,
        2,
    )

    return average


def sale_profit(db: Session, user_id: int):
    profit = round(
        db.query(func.sum(models.Items.price))
        .filter(models.Items.user_id == user_id, models.Items.sold != None)
        .scalar()
        / 100,
        2,
    )

    return profit


def biggest_profit(db: Session, user_id: int):
    query = text(
        f"SELECT title FROM items WHERE user_id={user_id} and sold IS NOT NULL and price = (SELECT MAX(price) FROM items);"
    )
    result = db.execute(query)
    items = []
    for r in result:
        items.append(r[0])

    if items:
        return items[0]
    return ""
