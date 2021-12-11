from unittest.mock import patch, call

from menu.menu import Entry


def test_create_entry():
    e = Entry.create('help', 'If you need help', lambda: None, False)
    assert e.key.value == 'help' and e.description.value == 'If you need help'


@patch('builtins.print')
def test_entry_on_selected(mocked_print):
    e = Entry.create('1', 'Say bye', lambda: print('Adios!'))
    e.on_selected()
    assert mocked_print.mock_calls == [call('Adios!')]
