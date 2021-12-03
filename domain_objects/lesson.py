from datetime import datetime, timedelta
from dataclasses import InitVar, dataclass, field
from enum import Enum, unique
from typing import Any
from typeguard import typechecked

from user import Student
from cost import Cost

@unique # Avoid to have aliases in the `Instrument` enum.
class Instrument(Enum):
	GUITAR = 0
	PIANO = 1
	DRUM = 2
	TRIANGLE = 3

@typechecked
@dataclass()
class Lesson:
	lesson_name: str
	teacher: str
	instrument: Instrument
	students: list(Student)
	date_time: datetime
	duration: timedelta
	cost: Cost

	create_key: InitVar[Any] = field(default=None)


	__create_key = object()

	def create(*args, **kwargs):
		pass
	
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

