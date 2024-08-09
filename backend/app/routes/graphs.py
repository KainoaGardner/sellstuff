from fastapi import HTTPException, APIRouter, Depends, Query
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session
from app.database.database import get_db
from app.functions import users, graphs
from app.functions.authentication import user_dependency

from datetime import date


router = APIRouter(prefix="/graphs", tags=["Graphs"])


@router.get("/sales_by_times")
def get_bar_graph(
    user_auth: user_dependency,
    db: Session = Depends(get_db),
    date: date = date.today(),
    value_type: str = Query("sales", enum=["sales", "profit"]),
    graph_type: str = Query("weekly", enum=["weekly", "monthly", "yearly"]),
    color: str = Query(
        "blue",
        enum=[
            "red",
            "orange",
            "yellow",
            "green",
            "blue",
            "purple",
            "black",
        ],
    ),
):
    user_id = user_auth["id"]

    image_path = graphs.bar(db, user_id, date, value_type, graph_type, color)

    return FileResponse(image_path)


@router.get("/profit_over_time")
def get_plot_graph(
    user_auth: user_dependency,
    db: Session = Depends(get_db),
    date: date = date.today(),
    graph_type: str = Query("weekly", enum=["weekly", "monthly", "yearly"]),
    color: str = Query(
        "blue",
        enum=[
            "red",
            "orange",
            "yellow",
            "green",
            "blue",
            "purple",
            "black",
        ],
    ),
):
    user_id = user_auth["id"]

    image_path = graphs.plot(db, user_id, date, graph_type, color)

    return FileResponse(image_path)
