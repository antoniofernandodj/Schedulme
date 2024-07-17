from dataclasses import dataclass
from schedule.conds import ScheduleCondition
from typing import Callable, List, Optional, Tuple


@dataclass
class Task:
    schedule_condition: ScheduleCondition
    func: Callable
    after_success: Optional[Callable] = None
    after_failure: Optional[Callable] = None
    always: Optional[Callable] = None


class Blueprint:
    def __init__(self, name) -> None:
        self.name = name
        self.tasks: List[Task] = []

    def register_blueprint(self, blueprint: "Blueprint"):
        for task in blueprint.tasks:
            self.tasks.append(task)

    def task(
        self,
        schedule: ScheduleCondition,
        after_success=None,
        after_failure=None,
        always=None,
    ):
        def decorator(func: Callable):
            task = Task(
                schedule_condition=schedule,
                func=func,
                after_success=after_success,
                after_failure=after_failure,
                always=always,
            )

            self.tasks.append(task)
            return task

        return decorator
