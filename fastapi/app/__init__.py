from fastapi import FastAPI

app = FastAPI()

from app.database.database import engine
import app.database.models as models

models.Base.metadata.create_all(bind=engine)

from app import routes
