from typing import Callable
from typeguard import typechecked
import re


# @typechecked
def pattern(regex: str) -> Callable[[str], bool]:
	r = re.compile(regex)

	def res(value):
		return bool(r.fullmatch(value))
	res.__name__ = f'pattern({regex})'
	return res
