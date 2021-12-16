from unittest.mock import patch

import pytest
from valid8 import ValidationError

from core.menu.menu import Menu, Description, Entry


def test_create_menu_without_exit_fails():
    with pytest.raises(ValidationError):
        Menu.Builder(Description('This is my menu')).build()


def test_create_simple_menu():
    Menu.Builder(Description('My Menu')).with_entry(Entry.create('0', 'Exit', lambda: None, True)).build()


def test_menu_builder_cannot_call_build_more_than_one_time():
    menu_builder = Menu.Builder(Description('My Description')).with_entry(Entry.create('1', 'One', is_exit=True))
    menu_builder.build()
    with pytest.raises(ValidationError):
        menu_builder.build()


def test_menu_no_duplicates():
    menu_builder = Menu.Builder(Description('My Description')).with_entry(Entry.create('1', 'One'))
    with pytest.raises(ValidationError):
        menu_builder.with_entry(Entry.create('1', 'One'))


@patch('builtins.input', side_effect=['A', '0'])
@patch('builtins.print')
def test_menu_call_on_selected(mocked_print, mocked_input):
    menu = Menu.Builder(Description('My beautiful menu'))\
        .with_entry(Entry.create('A', 'An entry for A', on_selected=lambda: print('A!')))\
        .with_entry(Entry.create('0', 'Exit', is_exit=True))\
        .build()
    menu.run()
    mocked_print.assert_any_call('A!')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['5', '0'])
@patch('builtins.print')
def test_menu_wrong_key(mocked_print, mocked_input):
    menu = Menu.Builder(Description('a description'))\
        .with_entry(Entry.create('1', 'My entry', on_selected=lambda: print('My entry selected')))\
        .with_entry(Entry.create('0', 'Exit', is_exit=True))\
        .build()
    menu.run()
    mocked_print.assert_any_call('Invalid entry selected. Please, select a valid option.')
    mocked_input.assert_called()


def dummy_function(exception):
    raise exception


@patch('builtins.input', side_effect=['1', '0'])
@patch('builtins.print')
def test_menu_invalid_input(mocked_print, mocked_input):
    menu = Menu.Builder(Description('a description')) \
        .with_entry(Entry.create('1', 'My entry', on_selected=lambda: dummy_function(ValueError()))) \
        .with_entry(Entry.create('0', 'Exit', is_exit=True)) \
        .build()
    menu.run()
    mocked_print.assert_any_call('Invalid input provided. Please, try again.')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['1', '0'])
@patch('builtins.print')
def test_menu_type_error(mocked_print, mocked_input):
    menu = Menu.Builder(Description('a description')) \
        .with_entry(Entry.create('1', 'My entry', on_selected=lambda: dummy_function(TypeError()))) \
        .with_entry(Entry.create('0', 'Exit', is_exit=True)) \
        .build()
    menu.run()
    mocked_print.assert_any_call('An internal validation failed. Please, report this error.')
    mocked_input.assert_called()

