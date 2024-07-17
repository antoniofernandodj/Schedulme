from datetime import datetime
import sys
import os

sys.path.append(os.getcwd())

from bp1 import bp1
from bp2 import bp2
from bp3 import bp3

from schedule import (
    Schedule,
    Every,
    Second,
)


app = Schedule(__name__)


app.register_blueprint(bp1)
app.register_blueprint(bp2)
app.register_blueprint(bp3)


@app.task(Every(Second()))
def app_test_every_second():
    print(f"Task test_every_second 1 executed at {datetime.now()}.")


@app.task(Every(Second))
def app_test_every_second():
    print(f"Task test_every_second 2 executed at {datetime.now()}.")


if __name__ == "__main__":
    app.run(debug=True, loop_time=1)
