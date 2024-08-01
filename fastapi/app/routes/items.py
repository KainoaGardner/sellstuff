from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import schemas
from app.database.database import get_db
from app.functions import items, users
from app.functions.authentication import user_dependency


router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/all", response_model=list[schemas.Item])
def get_all_items(user_auth: user_dependency, db: Session = Depends(get_db)):
    user_id = user_auth["id"]
    return users.get_user(db, user_id).items


@router.post("/create", response_model=schemas.Item)
def create_item(
    new_item: schemas.ItemBase,
    user_auth: user_dependency,
    db: Session = Depends(get_db),
):
    user_id = user_auth["id"]
    db_user = users.get_user(db, user_id)

    return items.put_new_item(db, db_user, new_item)


@router.put("/update", response_model=schemas.Item)
def update_item(
    user_auth: user_dependency,
    item_id: int,
    new_item: schemas.Item,
    db: Session = Depends(get_db),
):
    user_id = user_auth["id"]

    db_item = items.get_item(db, user_id, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return items.update_item(db, db_item, new_item)


@router.delete("/delete", response_model=schemas.Item)
def delete_item(
    user_auth: user_dependency, item_id: int, db: Session = Depends(get_db)
):
    user_id = user_auth["id"]
    item = items.get_item(db, user_id, item_id)
    return items.delete_item(db, item)
