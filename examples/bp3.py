from schedule import (
    Blueprint,
    Every,
    DayOfMonth,
    DayOfWeek,
)
from datetime import datetime


bp3 = Blueprint("bp3")


@bp3.task(Every(DayOfWeek(1)))
def bp3_test_every_day_of_week_1():
    print(f"Task test_every_day_of_week_0 executed at {datetime.now()}.")


@bp3.task(Every(DayOfMonth(5)))
def bp3_test_every_day_of_month_5():
    print(f"Task test_every_day_of_month_5 executed at {datetime.now()}.")
