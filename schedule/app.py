from datetime import datetime
import inspect
from time import sleep
from typing import List, Tuple, Callable, TypeGuard  # noqa
from threading import Thread

from schedule.utils import (
    print_bold_red,
    print_cyan_bright,
    print_green_bright,
    print_yellow,
)
from schedule.blueprint import Blueprint, Task
from schedule.conds import ScheduleCondition


class Schedule:
    def __init__(self, name: str) -> None:
        self.name = name
        self.tasks: List[Task] = []
        self.blueprints: List[Blueprint] = []
        self.resources_before = self.resources()
        self.resources_running = []

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
            return func

        return decorator

    def register_blueprint(self, blueprint: Blueprint):
        for task in blueprint.tasks:
            self.tasks.append(task)

    def display_tasks(self):
        print_cyan_bright("Scheduled Tasks:")
        for task in self.tasks:
            print_yellow(
                "Task: {}, Schedule: {}({})".format(
                    task.func.__name__,
                    task.schedule_condition.__class__.__name__,
                    task.schedule_condition.value,
                )
            )

    def __get_injected_params(self, task):
        injected_params = {}
        params_to_inject = {"scheduler": self, "task": task}
        sign = inspect.signature(task.func)

        for key, value in params_to_inject.items():
            if key in sign.parameters.keys():
                injected_params.update({key: value})

        return injected_params

    def run(self, debug: bool, loop_time: float = 1.0):
        self.loop_time = loop_time
        self.display_tasks()
        print_green_bright(f"Scheduler {self.name} is running...\n")  # noqa
        try:
            while True:
                if debug:
                    print(datetime.now())

                for task in self.tasks:

                    def func(task: Task):
                        if task.schedule_condition.matches(datetime.now()):
                            injected_params = self.__get_injected_params(task)
                            try:
                                value = task.func(**injected_params)
                                if task.after_success is not None:
                                    task.after_success.print = print_green_bright
                                    task.after_success(value)

                            except Exception as error:
                                if task.after_failure is not None:
                                    task.after_failure.print = print_bold_red
                                    task.after_failure(error)

                            finally:
                                if task.always is not None:
                                    task.always.print = print_cyan_bright
                                    task.always()

                    Thread(target=func, args=[task]).start()

                sleep(self.loop_time)

        except KeyboardInterrupt:
            import sys

            sys.exit(0)

    def resources(self):
        import psutil
        import os

        process_id = os.getpid()

        process = psutil.Process(process_id)
        memory_usage = process.memory_info().rss / 1024  # Em KB

        return memory_usage
