from datetime import datetime, timedelta
from dataclasses import InitVar, dataclass, field
from enum import Enum, unique
from typing import Any
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
	lesson_name: str
	teacher: str
	instrument: Instrument
	students: [Student]
	date_time: datetime
	duration: timedelta
	cost: Cost

	create_key: InitVar[Any] = field(default=None)

	__create_key = object()

	def __post_init__(self, create_key):
		validate('create_key', create_key, equals=self.__create_key)
		validate_dataclass(self)

	@staticmethod
	def create(lesson_name=None, teacher=None, instrument=None, students = [], date_time=None, duration=None, cost=None) -> 'Lesson':
		# validate('Lesson Arguments', args, min_len=6, max_len=6)
		# for x in args:
		# 	validate('Lesson Argument', x)
		return Lesson(lesson_name, teacher, instrument, students, date_time, duration, cost, Lesson.__create_key)
	
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

