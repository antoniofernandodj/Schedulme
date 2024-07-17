from datetime import datetime
from time import sleep
from typing import List, Tuple, Callable, TypeGuard  # noqa

from schedule.utils import print_cyan_bright, print_green_bright, print_yellow
from schedule.blueprint import Blueprint
from schedule.conds import ScheduleCondition


class Schedule:
    def __init__(self) -> None:
        self.tasks: List[Tuple[ScheduleCondition, Callable]] = []
        self.blueprints: List[Blueprint] = []

    def task(self, schedule: ScheduleCondition):
        def decorator(func: Callable):
            self.tasks.append((schedule, func))
            return func
        return decorator

    def register_blueprint(self, blueprint: Blueprint):
        for schedule, task in blueprint.tasks:
            self.tasks.append((schedule, task))

    def display_tasks(self):
        print_cyan_bright("Scheduled Tasks:")
        for schedule, task in self.tasks:
            print_yellow("Task: {}, Schedule: {}({})".format(
                task.__name__,
                schedule.__class__.__name__,
                schedule.value
            ))

    def run(self, debug: bool, loop_time: float = 1.0):
        self.display_tasks()
        print_green_bright(f"Scheduler is running...")  # noqa
        try:
            while True:
                if debug is True:
                    print(datetime.now())

                for schedule, task in self.tasks:
                    if schedule.matches(datetime.now()):
                        task()

                sleep(loop_time)
        except KeyboardInterrupt:
            import sys
            sys.exit(0)
