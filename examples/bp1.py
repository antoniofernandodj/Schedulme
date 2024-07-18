from schedule import (
    Schedule,
    Blueprint,
    Every,
    Time,
    Date,
    Once,
    Second,
)
from datetime import datetime
import time
import random

from schedule.blueprint import Task


bp1 = Blueprint("bp1")


def on_success(result):
    on_success.print("Sucesso: ", end="")
    on_success.print(result)


def on_error(error):
    on_error.print(":( Error: ", end="")
    on_error.print(error)


def always():
    always.print("This here always happen")


@bp1.task(
    schedule=Every(Second()),
    after_success=on_success,
    after_failure=on_error,
    always=always,
)
def bp1_test_every_second_with_callbacks(scheduler: Schedule, task: Task):
    # scheduler.loop_time += 1

    print("Executing long running task...")
    time.sleep(3)

    print(f"Task test_every_second_with_callbacks executed at {datetime.now()}.")  # noqa

    if random.random() > 0.5:
        print(3 / 0)

    return "Success!"


@bp1.task(schedule=Once(Date(day=10, month=8, year=2024)))
def bp1_test_once_date():
    print(f"Task test_once_date executed at {datetime.now()}.")
    return "Success!"


@bp1.task(Every(Time(hour=19, minute=44, second=0)))
def bp1_test_every_x_daytime():
    print(f"Task test_every_x_daytime ! executed at {datetime.now()}.")
