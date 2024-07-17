import abc
from datetime import date, datetime, time
from typing import Generic, List, Optional, Union, TypeVar, TypeGuard  # noqa

TimeConditionValueType = TypeVar('TimeConditionValueType')
ScheduleConditionValueType = Union[date, datetime, 'TimeCondition']


class TimeCondition(Generic[TimeConditionValueType], abc.ABC):

    value: TimeConditionValueType

    @abc.abstractmethod
    def matches(self, current_time: datetime) -> bool:
        pass


class ScheduleCondition(abc.ABC):
    value: ScheduleConditionValueType

    @abc.abstractmethod
    def matches(self, current_time: datetime) -> bool:
        pass


class Once(ScheduleCondition):

    executed: List['Once'] = []

    def __init__(self, value: ScheduleConditionValueType) -> None:
        if isinstance(value, date) and not isinstance(value, datetime):
            value = datetime.combine(value, datetime.min.time())
        self.value: ScheduleConditionValueType = value

    def matches(self, current_time: datetime) -> bool:
        if self in self.executed:
            return False

        elif isinstance(self.value, datetime):
            result = (self.value - current_time).seconds == 0

        elif isinstance(self.value, date):
            datetime_obj = datetime.combine(self.value, datetime.min.time())
            result = (datetime_obj - current_time).seconds == 0

        elif (
            not isinstance(self.value, datetime) and
            issubclass(type(self.value), TimeCondition)
        ):
            result = self.value.matches(current_time)

        else:
            raise NotImplementedError

        if result is True:
            self.executed.append(self)

        return result


class Every(ScheduleCondition):
    def __init__(self, value: ScheduleConditionValueType) -> None:
        self.value: ScheduleConditionValueType
        self.value = value

    def matches(self, current_time: datetime) -> bool:

        if isinstance(self.value, datetime):
            result = (self.value - current_time).seconds == 0

        elif isinstance(self.value, date):
            datetime_obj = datetime.combine(self.value, datetime.min.time())
            result = (datetime_obj - current_time).seconds == 0

        elif (
            not isinstance(self.value, datetime) and
            issubclass(type(self.value), TimeCondition)
        ):
            result = self.value.matches(current_time)

        else:
            raise NotImplementedError

        return result


class DayTime(TimeCondition):
    def __init__(self, hour: int, minute: int, second: int):
        self.time = time(hour, minute, second)

    def matches(self, current_time: datetime) -> bool:
        return current_time.time() == self.time

    def __str__(self):
        return f"{self.__class__.__name__}({self.time.strftime('%H:%M:%S')})"


class Second(TimeCondition):
    def __init__(self, value: Optional[int] = None):
        self.value = value

    def matches(self, current_time: datetime) -> bool:
        if self.value is None:
            return True
        return current_time.second == self.value

    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"


class Minute(TimeCondition):
    def __init__(self, value: int):
        self.value = value

    def matches(self, current_time: datetime) -> bool:
        return current_time.minute == self.value

    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"


class Hour(TimeCondition):
    def __init__(self, value: int):
        self.value = value

    def matches(self, current_time: datetime) -> bool:
        return current_time.hour == self.value

    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"


class DayOfWeek(TimeCondition):
    def __init__(self, value: int):
        self.value = value

    def matches(self, current_time: datetime) -> bool:
        return current_time.weekday() == self.value

    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"


class DayOfMonth(TimeCondition):
    def __init__(self, value: int):
        self.value = value

    def matches(self, current_time: datetime) -> bool:
        return current_time.day == self.value

    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"
