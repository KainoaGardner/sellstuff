from fastapi import HTTPException, APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from datetime import timedelta

from app.database.schemas import Token
from app.functions import users, authentication
from app.database.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/token/", response_model=Token)
def login_in_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = users.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Could not validate user")
    token = authentication.create_access_token(
        user.username, user.id, timedelta(days=7)
    )
    return {"access_token": token, "token_type": "bearer"}
