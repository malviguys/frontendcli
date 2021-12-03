from dataclasses import InitVar, dataclass, field
from typing import Any
from typeguard import typechecked
from valid8 import validate
from validation.dataclasses import validate_dataclass
import re


@typechecked
@dataclass()
class Cost:
	value_in_cents: int

	create_key: InitVar[Any] = field(default=None)

	__create_key = object()
	# Max value is set to (10^9)-1, since the `Cost` object is defined to handle 6 integer digits and 2 decimal digits
	__max_value = (10**9)-1
	# Pattern used for parsing
	__parse_pattern = re.compile(r'(?P<euro>:\d{0,6})\.(?P<cents>:\d{2})')

	def __post_init__(self, create_key):
		validate('create_key', create_key, equals=self.__create_key)
		validate_dataclass(self)
		validate('value_in_cents', self.value_in_cents, min_value=0, max_value=Cost.__max_value)
	
	def __str__(self) -> str:
		return f'{self.value_in_cents // 100}.{self.value_in_cents%100:02}'

	@staticmethod
	def create(euro: int, cents: int=0) -> 'Cost':
		validate('euro', euro, min_value=0, max_value=Cost.__max_value // 100)
		validate('cents', cents, min_value=0, max_value=99)
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
		return self.value_in_cents%100
	
	@property
	def euro(self) -> int:
		return self.value_in_cents // 100

