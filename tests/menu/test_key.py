import pytest
from valid8 import ValidationError

from menu.menu import Key


def test_create_key():
    k = Key('1')
    assert k.value == '1'


def test_key_str():
    val = 'help'
    assert str(Key(val)) == val


def test_key_empty_fails():
    with pytest.raises(ValidationError):
        Key('')


def test_key_special_chars_fail():
    for special_char in ['\n', '\r', '*', '^', '$', '€']:
        with pytest.raises(ValidationError):
            Key(special_char)


def test_key_integer_fails():
    with pytest.raises(TypeError):
        Key(0)


def test_key_too_long():
    with pytest.raises(ValidationError):
        Key('1'*11)
