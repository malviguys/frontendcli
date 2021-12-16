from dataclasses import InitVar, dataclass, field
from typing import Any
from typeguard import typechecked
from valid8 import validate
import re

from validation.dataclasses import validate_dataclass


#@typechecked
@dataclass(frozen=True, order=True)
class Cost:
	value_in_cents: int

	create_key: InitVar[Any] = field(default=None)

	__create_key = object()
	# Max value is set to (10^9)-1, since the `Cost` object is defined to handle 6 integer digits and 2 decimal digits
	__max_value_all = (10 ** 9) - 1
	__max_value_euros = __max_value_all // 100
	__max_value_cents = 99
	__min_value_euros = 0
	__min_value_cents = 0
	# Pattern used for parsing
	__parse_pattern = re.compile(r'(?P<euro>\d{1,6})\.(?P<cents>\d{1,2})')

	def __post_init__(self, create_key):
		validate('Cost.create_key', create_key, equals=self.__create_key)
		validate_dataclass(self)
		validate('value_in_cents', self.value_in_cents, min_value=0, max_value=Cost.__max_value_all)
	
	def __str__(self) -> str:
		return f'{self.value_in_cents // 100}.{self.value_in_cents%100:02}'

	@staticmethod
	def create(euro: int, cents: int=0) -> 'Cost':
		validate('euro', euro, min_value=Cost.__min_value_euros, max_value=Cost.__max_value_euros)
		validate('cents', cents, min_value=Cost.__min_value_cents, max_value=Cost.__max_value_cents)
		return Cost((euro*100) + cents, Cost.__create_key)

	@staticmethod
	def parse(value: str) -> 'Cost':
		m = Cost.__parse_pattern.fullmatch(value)
		validate('value', m)
		euro = m.group('euro')
		cents = m.group('cents') if m.group('cents') else 0
		return Cost.create(int(euro), int(cents))
	
	@property
	def cents(self) -> int:
		return self.value_in_cents % 100
	
	@property
	def euro(self) -> int:
		return self.value_in_cents // 100

