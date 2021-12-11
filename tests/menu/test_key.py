from menu.menu import Key


def test_create_key():
    k = Key('1')
    assert k.value == '1'


def test_key_str():
    val = 'help'
    k = Key(val)
    assert k.__str__() == val
