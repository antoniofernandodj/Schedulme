from schedulme import (
    Blueprint,
    Every,
    Hour,
    Second,
    N_Seconds,
    N_Minutes,
    N_Hours
)
from datetime import datetime


bp2 = Blueprint("bp2")


bp2_1 = Blueprint("bp2_1")
bp2_2 = Blueprint("bp2_2")


@bp2_1.task(Every(Second(30)))
def bp2_1_test_every_second_30():
    print(f"Task test_every_second_30 executed at {datetime.now()}.")


# Ainda não está bom
@bp2_1.task(Every(N_Seconds(5, bp2_1)))
def bp2_1_test_every_5_seconds():
    print(f"Task test_every_5_seconds executed at {datetime.now()}.")


# Ainda não está bom
@bp2_2.task(Every(N_Minutes(2, bp2_1)))
def bp2_2_test_every_2_minutes():
    print(f"Task test_every_2_minutes executed at {datetime.now()}.")


# Ainda não está bom
@bp2.task(Every(N_Hours(2, bp2_1)))
def bp2_test_every_2_hours():
    print(f"Task test_every_2_hour executed at {datetime.now()}.")


@bp2.task(Every(Hour(4)))
def bp2_test_every_hour_4():
    print(f"Task test_every_hour_4 executed at {datetime.now()}.")


bp2.register_blueprint(bp2_1)
bp2.register_blueprint(bp2_2)
