from schedule import (
    Blueprint,
    Every,
    Hour,
    Second,
)
from datetime import datetime


bp2 = Blueprint("bp2")


bp2_1 = Blueprint("bp2_1")
bp2_2 = Blueprint("bp2_2")


@bp2_1.task(Every(Second(30)))
def bp2_1_test_every_second_30():
    print(f"Task test_every_second_30 executed at {datetime.now()}.")


# # Esta executando varias vezes caso o minuto seja 30.
# # seria interessante apenas uma vez
# @bp2_2.task(Every(Minutes(30)))
# def bp2_2_test_every_minute_30():
#     print(f"Task test_every_minute_30 executed at {datetime.now()}.")


@bp2.task(Every(Hour(4)))
def bp2_test_every_hour_4():
    print(f"Task test_every_hour_4 executed at {datetime.now()}.")


bp2.register_blueprint(bp2_1)
bp2.register_blueprint(bp2_2)
