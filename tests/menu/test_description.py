import pytest
from valid8 import ValidationError

from menu.menu import Description


def test_create_description():
    d = Description('Test')
    assert d.value == 'Test'


def test_description_str():
    text = 'This is my pretty description'
    d = Description(text)
    assert d.__str__() == text


def test_description_empty_fails():
    with pytest.raises(ValidationError):
        Description('')


def test_description_special_chars_fail():
    for special_char in ['\n', '\r', '*', '^', '$', '€']:
        with pytest.raises(ValidationError):
            Description(special_char)


def test_description_too_long():
    with pytest.raises(ValidationError):
        Description('z'*2001)