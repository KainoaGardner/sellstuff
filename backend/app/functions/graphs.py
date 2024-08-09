from sqlalchemy import text
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from app.database import models
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import matplotlib.pyplot as plt
from app.other import weekday, colors


def bar(
    db: Session,
    user_id: int,
    today_date: date,
    value_type: str,
    graph_type: str,
    color: str,
):
    match graph_type:
        case "weekly":
            return sales_by_week(db, user_id, today_date, value_type, color)
        case "monthly":
            return sales_by_month(db, user_id, today_date, value_type, color)
        case "yearly":
            return sales_by_year(db, user_id, today_date, value_type, color)


def plot(
    db: Session,
    user_id: int,
    today_date: date,
    graph_type: str,
    color: str,
):
    match graph_type:
        case "weekly":
            return profit_by_week_plot(db, user_id, today_date, color)
        case "monthly":
            return profit_by_month_plot(db, user_id, today_date, color)
        case "yearly":
            return profit_by_year_plot(db, user_id, today_date, color)


def sales_by_week(db, user_id, today_date, value_type, color):
    start_date = today_date - relativedelta(days=+7)

    datelist = pd.date_range(start_date + relativedelta(days=+1), today_date)
    x = []
    y = []
    for date in datelist:
        x.append(weekday[date.weekday()])
        if value_type == "sales":
            y.append(date_count(db, user_id, date, date))
        else:
            y.append(date_sum(db, user_id, date, date))

    if value_type == "sales":
        make_bar_graph(user_id, x, y, "Days", "Sales", "Sales per Day", color)
    else:
        make_bar_graph(user_id, x, y, "Days", "Profit $", "Profit per Day", color)

    return f"images/{user_id}/bar.png"


def make_bar_graph(user_id, x, y, x_type, y_type, title, color):
    fig = plt.figure(figsize=(10, 5), facecolor=colors["white"])
    plt.bar(x, y, color=colors[color])
    plt.xlabel(x_type)
    plt.ylabel(y_type)
    plt.title(title)
    plt.savefig(f"images/{user_id}/bar.png", bbox_inches="tight")


def make_plot_graph(user_id, x, y, x_type, y_type, title, color, start_date, end_date):
    print("test")
    fig = plt.figure(figsize=(10, 5), facecolor=colors["white"])
    ax = plt.gca()
    ax.set_xlim([start_date, end_date])
    plt.step(x, y, color=colors[color], where="post")
    plt.xlabel(x_type)
    plt.ylabel(y_type)
    ax.set_ylim(ymin=0)
    plt.title(title)
    plt.savefig(f"images/{user_id}/plot.png", bbox_inches="tight")


def date_count(db, user_id, start_date, end_date):
    return (
        db.query(func.count())
        .filter(
            models.Items.user_id == user_id,
            models.Items.sold >= start_date,
            models.Items.sold <= end_date,
        )
        .scalar()
    )


def date_sum(db, user_id, start_date, end_date):
    sum = (
        db.query(func.sum(models.Items.price))
        .filter(
            models.Items.user_id == user_id,
            models.Items.sold >= start_date,
            models.Items.sold <= end_date,
        )
        .scalar()
    )

    if sum:
        return sum / 100
    return 0


def sales_by_month(db, user_id, today_date, value_type, color):
    start_date = datetime(today_date.year, today_date.month, 1)
    datelist = []
    for i in range(3):
        datelist.append(
            [
                start_date + relativedelta(weeks=+i),
                start_date + relativedelta(weeks=+i + 1),
            ]
        )
    datelist.append(
        [
            start_date + relativedelta(weeks=+3),
            datetime(today_date.year, today_date.month + 1, 1),
        ]
    )

    x = [
        "Week 1",
        "Week 2",
        "Week 3",
        "Week 4",
    ]
    y = []
    for start, end in datelist:
        if value_type == "sales":
            y.append(date_count(db, user_id, start, end))
        else:
            y.append(date_sum(db, user_id, start, end))

    if value_type == "sales":
        make_bar_graph(user_id, x, y, "Days", "Sales", "Sales each Day", color)
    else:
        make_bar_graph(user_id, x, y, "Days", "Profit $", "Profit per Day", color)

    return f"images/{user_id}/bar.png"


def sales_by_year(db, user_id, today_date, value_type, color):
    start_date = datetime(today_date.year, 1, 1)
    datelist = []
    for i in range(12):
        datelist.append(
            [
                start_date + relativedelta(months=+i),
                start_date + relativedelta(months=+i + 1),
            ]
        )

    x = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    y = []
    for start, end in datelist:
        if value_type == "sales":
            y.append(date_count(db, user_id, start, end))
        else:
            y.append(date_sum(db, user_id, start, end))

    if value_type == "sales":
        make_bar_graph(user_id, x, y, "Months", "Sales", "Sales per Month", color)
    else:
        make_bar_graph(user_id, x, y, "Months", "Profit $", "Profit per Month", color)

    return f"images/{user_id}/bar.png"


def profit_by_week_plot(db, user_id, today_date, color):
    start_date = today_date - relativedelta(days=+7)

    sold_dates = get_sold_dates(db, user_id, start_date, today_date)
    start_profit = get_start_profit(db, user_id, start_date)
    x = [date[1] for date in sold_dates]
    y = get_profit_sum([date[0] / 100 for date in sold_dates], start_profit)
    x.insert(0, start_date)
    y.insert(0, start_profit)

    make_plot_graph(
        user_id,
        x,
        y,
        "Days",
        "Profit",
        "Past Week Profit",
        color,
        start_date,
        today_date,
    )
    return f"images/{user_id}/plot.png"


def profit_by_month_plot(db, user_id, today_date, color):
    start_date = today_date - relativedelta(months=+1)

    sold_dates = get_sold_dates(db, user_id, start_date, today_date)
    start_profit = get_start_profit(db, user_id, start_date)

    x = [date[1] for date in sold_dates]
    y = get_profit_sum([date[0] / 100 for date in sold_dates], start_profit)
    x.insert(0, start_date)
    y.insert(0, start_profit)

    make_plot_graph(
        user_id,
        x,
        y,
        "Days",
        "Profit",
        "Past Month Profit",
        color,
        start_date,
        today_date,
    )
    return f"images/{user_id}/plot.png"


def profit_by_year_plot(db, user_id, today_date, color):
    start_date = today_date - relativedelta(years=+1)

    sold_dates = get_sold_dates(db, user_id, start_date, today_date)
    start_profit = get_start_profit(db, user_id, start_date)
    x = [date[1] for date in sold_dates]
    y = get_profit_sum([date[0] / 100 for date in sold_dates], start_profit)
    x.insert(0, start_date)
    y.insert(0, start_profit)

    make_plot_graph(
        user_id,
        x,
        y,
        "Days",
        "Sales",
        "Past Year Profit",
        color,
        start_date,
        today_date,
    )
    return f"images/{user_id}/plot.png"


def get_profit_sum(prices, start_profit):
    total_sum = start_profit
    profit_sum = []
    for i in range(len(prices)):
        profit_sum.append(prices[i] + total_sum)
        total_sum += prices[i]
    return profit_sum


def get_sold_dates(db, user_id, start_date, end_date):
    return (
        db.query(models.Items.price, models.Items.sold)
        .filter(
            models.Items.user_id == user_id,
            models.Items.sold >= start_date,
            models.Items.sold <= end_date,
        )
        .order_by(models.Items.sold)
        .all()
    )


def get_start_profit(db, user_id, start_date):
    sum = (
        db.query(func.sum(models.Items.price))
        .filter(
            models.Items.user_id == user_id,
            models.Items.sold < start_date,
        )
        .scalar()
    )

    if sum:
        return sum / 100
    return 0
