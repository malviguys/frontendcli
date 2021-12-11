import pytest
from valid8 import ValidationError

from menu.menu import Menu, Description, Entry


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


# TODO: belongs to test for app
# def test_menu_does_not_crash_on_run():
#     m = Menu.Builder(Description('My Menu')).with_entry(Entry.create('0', 'Exit', lambda: None, True)).build()
#     m.run()
#