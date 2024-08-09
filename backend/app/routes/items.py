from fastapi import HTTPException, APIRouter, Depends, Query, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import schemas
from app.database.database import get_db
from app.functions import items, users
from app.functions.authentication import user_dependency
import os

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/all", response_model=list[schemas.Item])
def get_all_items(
    user_auth: user_dependency,
    db: Session = Depends(get_db),
    sort: str = Query("id", enum=["id", "title", "price", "sold_date"]),
    reverse_sort: bool | None = False,
):

    user_id = user_auth["id"]
    user_items = items.get_all_items(db, user_id, sort, reverse_sort)

    for item in user_items:
        item.price /= 100

    return user_items


@router.get("/image")
def get_image(
    # user_auth: user_dependency,
    item_id: int,
    db: Session = Depends(get_db),
):
    db_item = items.get_item(db, item_id)

    if not db_item or not db_item.image:
        raise HTTPException(status_code=404, detail="No Image")

    return FileResponse(f"images/{db_item.image}")


@router.put("/toggle_sold", response_model=schemas.Item)
def toggle_sold(
    user_auth: user_dependency,
    item_id: int,
    db: Session = Depends(get_db),
):

    db_item = items.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    item = items.toggle_sold(db, db_item)
    item.price /= 100
    return item


@router.put("/image")
def put_image(
    user_auth: user_dependency,
    item_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if file.content_type not in [
        "image/jpeg",
        "image/png",
        "image/vnd.microsoft.icon",
        "image/webp",
    ]:
        raise HTTPException(404, detail="Invalid image type")

    user_id = user_auth["id"]
    db_item = items.get_item(db, item_id)

    if not db_item:
        raise HTTPException(status_code=404, detail="No Image")

    try:
        contents = file.file.read()
        file_type = os.path.splitext(file.filename)[1]
        path = f"{user_id}/{item_id}{file_type}"
        os.makedirs(os.path.dirname(f"images/{path}"), exist_ok=True)
        with open(f"images/{path}", "wb") as f:
            f.write(contents)

        items.put_image(db, db_item, path)
        return FileResponse(f"images/{path}")
    except Exception:
        print(Exception)
        raise HTTPException(status_code=404, detail="Image Upload Error")
    finally:
        file.file.close()


@router.put("/update", response_model=schemas.Item)
def update_item(
    user_auth: user_dependency,
    item_id: int,
    new_item: schemas.ItemChange,
    db: Session = Depends(get_db),
):

    db_item = items.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    item = items.update_item(db, db_item, new_item)
    item.price /= 100
    return item


@router.post("/create", response_model=schemas.Item)
def create_item(
    new_item: schemas.ItemBase,
    user_auth: user_dependency,
    db: Session = Depends(get_db),
):
    user_id = user_auth["id"]

    item = items.put_new_item(db, user_id, new_item)
    item.price /= 100
    return item


@router.delete("/delete", response_model=schemas.Item)
def delete_item(
    user_auth: user_dependency, item_id: int, db: Session = Depends(get_db)
):
    db_item = items.get_item(db, item_id)

    item = items.delete_item(db, db_item)
    item.price /= 100
    return item
