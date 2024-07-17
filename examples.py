from datetime import datetime, date
from schedule import (
    Schedule,
    Blueprint,
    Every,
    DayTime,
    Once,
    Minute,
    Hour,
    Second,
    DayOfMonth,
    DayOfWeek,
)

sched = Schedule()

bp1 = Blueprint()
bp2 = Blueprint()
bp3 = Blueprint()


def callback1(result):
    print(result)


def callback2(error):
    print(error)


@bp1.task(
    Once(date(day=10, month=8, year=2024)),
    after_success=callback1,
    after_failure=callback2,
)
def test_once_date():
    print(f"Task test_once_date executed at {datetime.now()}.")


@bp1.task(
    Once(datetime(hour=12, minute=0, second=0, day=10, month=8, year=2024))
)  # noqa
def test_once_datetime():
    print(f"Task test_once_datetime executed at {datetime.now()}.")


@bp1.task(Every(DayTime(hour=12, minute=0, second=0)))
def test_every_x_daytime():
    print(f"Task test_every_x_daytime executed at {datetime.now()}.")


@bp2.task(Every(Second(30)))
def test_every_second_30():
    print(f"Task test_every_second_30 executed at {datetime.now()}.")


# Esta executando varias vezes caso o minuto seja 30.
# seria interessante apenas uma vez
@bp2.task(Every(Minute(30)))
def test_every_minute_30():
    print(f"Task test_every_minute_30 executed at {datetime.now()}.")


@bp2.task(Every(Hour(4)))
def test_every_hour_4():
    print(f"Task test_every_hour_4 executed at {datetime.now()}.")


@bp3.task(Every(DayOfWeek(0)))
def test_every_day_of_week_0():
    print(f"Task test_every_day_of_week_0 executed at {datetime.now()}.")


@bp3.task(Every(DayOfMonth(5)))
def test_every_day_of_month_5():
    print(f"Task test_every_day_of_month_5 executed at {datetime.now()}.")


@sched.task(Every(Second()))
def test_every_second():
    print(f"Task test_every_second executed at {datetime.now()}.")


sched.register_blueprint(bp1)
sched.register_blueprint(bp2)
sched.register_blueprint(bp3)


sched.run(debug=False, loop_time=1)
