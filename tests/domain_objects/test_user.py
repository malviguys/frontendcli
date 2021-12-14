import pytest
from valid8 import ValidationError

from domain_objects.user import Username, User


def test_username():
    assert Username('Username').value == 'Username'


def test_username_str():
    assert str(Username('Username')) == 'Username'


def test_username_too_long():
    with pytest.raises(ValidationError):
        Username('a'*21)


def test_username_too_short():
    with pytest.raises(ValidationError):
        Username('a'*2)


def test_username_does_neither_start_nor_end_with_underscore_or_dot():
    for special_char in ['_', '.']:
        with pytest.raises(ValidationError):
            Username(special_char + 'abc')
        with pytest.raises(ValidationError):
            Username('abc' + special_char)


def test_username_no_special_chars_inside():
    for special_char in ['\n', '\r', '*', '^', '$', '€', '@', '__', '..']:
        with pytest.raises(ValidationError):
            Username('ab' + special_char + 'c')


def test_user_default_not_admin():
    user = User.create('Username', 'ImmaToken123')
    assert str(user.username) == 'Username' and user.token == 'ImmaToken123' and user.is_admin is False


# TODO: tests for token
