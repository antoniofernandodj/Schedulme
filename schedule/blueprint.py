from schedule.conds import ScheduleCondition
from typing import Callable, List, Tuple


class Blueprint:
    def __init__(self) -> None:
        self.tasks: List[Tuple[ScheduleCondition, Callable]] = []

    def task(self, schedule: ScheduleCondition):
        def decorator(func: Callable):
            self.tasks.append((schedule, func))
            return func
        return decorator
