from unittest.mock import patch, call, Mock

import pytest
from valid8 import ValidationError

from menu.menu import Entry


def test_create_entry():
    e = Entry.create('help', 'If you need help', lambda: None, False)
    assert e.key.value == 'help' and e.description.value == 'If you need help'


def test_entry_on_selected():
    mocked_on_selected = Mock()
    entry = Entry.create('1', 'Say hi', lambda: mocked_on_selected(), False)
    entry.on_selected()
    mocked_on_selected.assert_called_once()


@patch('builtins.print')
def test_entry_on_selected_print(mocked_print):
    e = Entry.create('1', 'Say bye', lambda: print('Adios!'))
    e.on_selected()
    assert mocked_print.mock_calls == [call('Adios!')]
