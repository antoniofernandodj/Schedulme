import abc
from datetime import date, datetime, time
from typing import Any, Dict, Generic, List, Optional, TypeVar, TypeGuard  # noqa


ConditionValueType = TypeVar("ConditionValueType")


class Condition(Generic[ConditionValueType], abc.ABC):

    value: ConditionValueType

    @abc.abstractmethod
    def matches(self, current_time: datetime) -> bool:
        pass


class Time(Condition):
    def __init__(self, hour: int, minute: int, second: int):
        self.time = time(hour, minute, second)

    def matches(self, current_time: datetime) -> bool:

        c = current_time
        t = self.time
        return (
            c.hour == t.hour and
            c.minute == t.minute and
            c.second == t.second
        )

    def __str__(self):
        return f"{self.__class__.__name__}({self.time.strftime('%H:%M:%S')})"


class Date(Condition):
    def __init__(self, day: int, month: int, year: int):
        self.date = date(year, month, day)

    def matches(self, current_time: datetime) -> bool:
        if not isinstance(current_time, datetime):
            raise TypeError

        return current_time == self.date

    def __str__(self):
        return f"{self.__class__.__name__}({self.date})"


class Once(Condition):

    executed: List["Once"] = []

    def __init__(self, value: Condition) -> None:

        self.value: Condition = value

    def matches(self, current_time: datetime) -> bool:
        if self in self.executed:
            return False

        else:
            result = self.value.matches(current_time)  # type: ignore

        if result is True:
            self.executed.append(self)

        return result


class Every(Condition):
    def __init__(self, value: Condition) -> None:  # type: ignore
        self.value: Condition = value

    def matches(self, current_time: datetime) -> bool:

        result = self.value.matches(current_time)  # type: ignore

        return result


GenericTimeValue = TypeVar('GenericTimeValue')


class Between(Condition):
    def __init__(self, t1: 'GenericTimeValue', t2: 'GenericTimeValue') -> None:
        self.value: GenericTimeValue = t1
        self.value2: GenericTimeValue = t2

    def matches(self, current_time: datetime) -> bool:
        if isinstance(self.value, Time) and isinstance(self.value2, Time):

            t1 = self.value.time
            t2 = self.value2.time

            return t1 <= current_time.time() <= t2

        elif isinstance(self.value, Date) and isinstance(self.value2, Date):

            d1 = self.value.date
            d2 = self.value2.date

            return d1 <= current_time <= d2

        else:
            raise TypeError

    def __str__(self):
        return f"{self.__class__.__name__}({self.value}, {self.value2})"


class After(Condition):
    def __init__(
        self, value: Any,
    ) -> None:
        self.value: Any = value

    def matches(self, current_time: datetime) -> bool:
        if isinstance(self.value, Time):
            ct = current_time.time()
            return self.value.time < ct

        elif isinstance(self.value, Date):
            cd = current_time.date()
            return self.value.date < cd

        else:
            raise TypeError

    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"


class Daily(Condition):
    days_executed: Dict[date, Condition] = {}

    def __init__(self, value: Condition) -> None:
        self.value: Condition = value

    def matches(self, current_time: datetime) -> bool:
        if self.days_executed.get(date.today()) is self.value:
            return False

        result = self.value.matches(current_time)  # type: ignore

        if result is True:
            self.days_executed[date.today()] = self.value

        return True


class Weekly(Condition):
    def __init__(self, value: Condition) -> None:
        self.value: Condition = value
        self.last_execution: Optional[date] = None

    def matches(self, current_time: datetime) -> bool:
        if not isinstance(current_time, datetime):
            raise TypeError

        today = current_time.date()
        if (
            self.last_execution is None or
            (today - self.last_execution).days >= 7
        ):
            if self.value.matches(current_time):
                self.last_execution = today
                return True
        return False


class Monthly(Condition):
    def __init__(self, value: Condition) -> None:
        self.value: Condition = value
        self.last_execution: Optional[date] = None

    def matches(self, current_time: datetime) -> bool:
        if not isinstance(current_time, datetime):
            raise TypeError

        today = current_time.date()
        if (
            self.last_execution is None or
            (today.year, today.month) != (
                self.last_execution.year, self.last_execution.month
            )
        ):
            if self.value.matches(current_time):
                self.last_execution = today
                return True
        return False


class Second(Condition):
    def __init__(self, value: Optional[int] = None):
        self.value = value

    def matches(self, current_time: datetime) -> bool:
        if self.value is None:
            return True

        return current_time.second == self.value

    def __str__(self):
        if self.value is None:
            return f"{self.__class__.__name__}"

        return f"{self.__class__.__name__}({self.value})"


class Hour(Condition):
    def __init__(self, value: int):
        self.value = value

    def matches(self, current_time: datetime) -> bool:
        if not isinstance(current_time, (datetime, time)):
            raise TypeError

        return current_time.hour == self.value

    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"


class DayOfWeek(Condition):
    def __init__(self, value: int):
        self.value = value

    def matches(self, current_time: datetime) -> bool:
        if not isinstance(current_time, (datetime, date)):
            raise TypeError

        return current_time.weekday() == self.value

    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"


class DayOfMonth(Condition):
    def __init__(self, value: int):
        self.value = value

    def matches(self, current_time: datetime) -> bool:
        return current_time.day == self.value

    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"


class N_Seconds(Condition):
    def __init__(self, value: int):
        from schedulme.app import Schedulme
        self.value = value

        self.start_time = Schedulme.state['start_time']

    def matches(self, current_time: datetime) -> bool:
        delta_time = self.start_time.second - current_time.second
        return delta_time % self.value == 0  # noqa
        return current_time.second % self.value == 0

    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"


class N_Minutes(Condition):
    def __init__(self, value: int):
        from schedulme.app import Schedulme
        self.value = value
        self.start_time = Schedulme.state['start_time']

    def matches(self, current_time: datetime) -> bool:
        delta_time = self.start_time.minute - current_time.minute
        return delta_time % self.value == 0
        return current_time.minute % self.value == 0

    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"


class N_Hours(Condition):
    def __init__(self, value: int):
        from schedulme.app import Schedulme
        self.value = value
        self.start_time = Schedulme.state['start_time']

    def matches(self, current_time: datetime) -> bool:
        delta_time = self.start_time.hour - current_time.hour
        return delta_time % self.value == 0
        return current_time.hour % self.value == 0

    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"
