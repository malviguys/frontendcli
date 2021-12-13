import re

from datetime import datetime, timedelta
from dataclasses import InitVar, dataclass, field
from enum import Enum, unique
from typing import Any, List
from typeguard import typechecked
from valid8.entry_points_inline import validate

from domain_objects.user import Student
from domain_objects.cost import Cost
from validation.dataclasses import validate_dataclass


@unique # Avoid to have aliases in the `Instrument` enum.
class Instrument(Enum):
    GUITAR = 0
    PIANO = 1
    DRUM = 2
    TRIANGLE = 3


@typechecked
@dataclass(frozen=True)
class Lesson:
    _lesson_name: str
    _teacher: str
    _instrument: Instrument
    _students: List[Student]
    _date_time: datetime
    _duration: timedelta
    _cost: Cost

    create_key: InitVar[Any] = field(default=None)

    __create_key = object()
    __name_max_length = 40
    __name_min_length = 2
    __name_pattern = re.compile(r'(?P<lesson_name>^[a-zA-Z][a-zA-Z\d -]{'
                                + re.escape(str(__name_min_length - 1)) + r','
                                + re.escape(str(__name_max_length - 1)) + r'})')
    __teacher_min_length = 5
    __teacher_max_length = 80
    __teacher_pattern = re.compile(r'(?P<teacher>([a-zA-Z-]{2,8}\. ?){0,5}( ?[A-Z][a-z]+){2,80})')
    __delta_time_min_weeks = 1
    __delta_time_max_weeks = 104
    __duration_min = 1
    __duration_max = 4

    def __post_init__(self, create_key):
        validate('create_key', create_key, equals=self.__create_key)
        validate_dataclass(self)

    @staticmethod
    def create(lesson_name=None, teacher=None, instrument=None, students=None, date_time=None, duration=None, cost=None) -> 'Lesson':
        # TODO: add error messages
        m_name = Lesson.__name_pattern.fullmatch(lesson_name)
        validate('lesson_name', m_name)
        validate('teacher', len(teacher), min_value=Lesson.__teacher_min_length, max_value=Lesson.__teacher_max_length)
        m_teacher = Lesson.__teacher_pattern.fullmatch(teacher)
        validate('teacher', m_teacher)
        # date_time should not be in past and should be at least 1 week in the future
        # and must not be more than 2 years in the future
        if date_time.date() < (datetime.now() + timedelta(weeks=Lesson.__delta_time_min_weeks)).date()\
            or date_time.date() > (datetime.now() + timedelta(weeks=Lesson.__delta_time_max_weeks)).date():
            raise ValueError("New lessons must be scheduled at least one week and not more than two years from now!")
        if duration < timedelta(hours=Lesson.__duration_min)\
            or duration > timedelta(hours=Lesson.__duration_max):
            raise ValueError("Lessons can have a duration only between "
                                + str(Lesson.__duration_min) + " and " + str(Lesson.__duration_max) + " hours!")
        return Lesson(lesson_name, teacher, instrument, students, date_time, duration, cost, Lesson.__create_key)

    def __str__(self) -> str:
        return f'Lesson {self.lesson_name}: \n\tPresented By: {self.teacher} \n\tInstrument: {self.instrument.name} ' \
                f'\n\tScheduled At: {self.date_time} \n\tDuration: {self.duration} hours \n\tCost: {self.cost.__str__()}€ ' \
                f'\n\tRegistered Students: {self.students}'

    @property
    def lesson_name(self): return self._lesson_name
    @property
    def teacher(self): return self._teacher
    @property
    def instrument(self): return self._instrument
    @property
    def students(self): return self._students
    @property
    def date_time(self): return self._date_time
    @property
    def duration(self): return self._duration
    @property
    def cost(self): return self._cost

