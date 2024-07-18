from schedulme import (
    Blueprint,
    Every,
    DayOfMonth,
    DayOfWeek,
    Time,
    Between,
    After
)
from datetime import datetime

from schedulme.conds import Once


bp3 = Blueprint("bp3")


@bp3.task(Every(DayOfWeek(1)))
def bp3_test_every_day_of_week_1():
    print(f"Task test_every_day_of_week_0 executed at {datetime.now()}.")


@bp3.task(Every(DayOfMonth(5)))
def bp3_test_every_day_of_month_5():
    print(f"Task test_every_day_of_month_5 executed at {datetime.now()}.")


@bp3.task(
    Once(
        Between(
            Time(hour=0, minute=0, second=0),
            Time(hour=1, minute=0, second=0)
        )
    )
)
def bp3_test_once_between_12_and_13():
    print(f"Task t1 executed at {datetime.now()}.")


@bp3.task(Once(After(Time(hour=0, minute=41, second=30))))
def bp3_test_once_after_12_00():
    print(f"Task t2 executed at {datetime.now()}.")
