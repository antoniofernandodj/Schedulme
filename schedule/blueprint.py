from dataclasses import dataclass
from datetime import datetime
from schedule.conds import Condition
from typing import Callable, List, Optional


@dataclass
class Task:
    condition: Condition
    func: Callable
    after_success: Optional[Callable] = None
    after_failure: Optional[Callable] = None
    always: Optional[Callable] = None


class Blueprint:
    def __init__(self, name) -> None:
        self.name = name
        self.tasks: List[Task] = []
        self.start_time = datetime.now()

    def register_blueprint(self, blueprint: "Blueprint"):
        for task in blueprint.tasks:
            self.tasks.append(task)

    def task(
        self,
        schedule: Condition,
        after_success=None,
        after_failure=None,
        always=None,
    ):
        def decorator(func: Callable):
            task = Task(
                condition=schedule,
                func=func,
                after_success=after_success,
                after_failure=after_failure,
                always=always,
            )

            self.tasks.append(task)
            return task

        return decorator
