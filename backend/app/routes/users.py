from fastapi import HTTPException, APIRouter, Depends
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session
from app.database import schemas
from app.database.database import get_db
from app.functions import users
from app.functions.authentication import user_dependency


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=schemas.User)
def get_current_user(user_auth: user_dependency, db: Session = Depends(get_db)):
    return user_auth


@router.get("/all", response_model=list[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    db_user = users.get_all_users(db)
    return db_user


@router.get("/data", response_model=schemas.Data)
def get_user_data(
    user_auth: user_dependency,
    db: Session = Depends(get_db),
):
    user_id = user_auth["id"]

    user_data = users.get_data(db, user_id)

    return user_data


@router.post("/create", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = users.get_user_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    return users.create_user(db, user)


@router.delete("/delete", response_model=schemas.User)
def delete_user(user_auth: user_dependency, db: Session = Depends(get_db)):
    user_id = user_auth["id"]
    db_user = users.get_user(db, user_id)

    return users.remove_user(db, db_user)
