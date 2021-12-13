from dataclasses import dataclass

import requests
from typeguard import typechecked
from valid8.entry_points_inline import validate

from validation.dataclasses import validate_dataclass
from validation.regex import pattern


@typechecked
@dataclass(frozen=True, order=True)
class Username:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        # The pattern will ensure that the username is between 3 and 20 chars long and does not contain underscores
        # and dot nor consequently nor at both ends
        # See https://stackoverflow.com/a/12019115/10301322 for more details
        validate('Username.value', self.value, min_len=3, max_len=20, custom=pattern(r'^(?=.{3,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$'))

    def __str__(self) -> str:
        return self.value


@typechecked
@dataclass(frozen=True)
class User:
    is_admin: bool
    username: Username
    token: str

    @property
    def username(self) -> str:
        return str(self.username)
    
    @property
    def token(self) -> str:
        return self.token

# TODO: What to define in the subclasses?

@typechecked
@dataclass(frozen=True, order=True)
class Student(User):
    pass

@typechecked
@dataclass(frozen=True, order=True)
class Teacher(User):
    pass


@typechecked
@dataclass(frozen=True, order=True)
class Admin(User):
    pass
