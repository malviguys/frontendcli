from menu.menu import Description

# TODO: ass validation testing


def test_create_description():
    d = Description('Test')
    assert d.value == 'Test'


def test_description_str():
    text = 'This is my pretty description'
    d = Description(text)
    assert d.__str__() == text

