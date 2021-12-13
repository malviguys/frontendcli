from unittest.mock import patch

from core.app import App


def test_create_app():
    App()


@patch('builtins.print')
def test_app_asks_for_login(mocked_print):
    App().run()
    line = 'Please, select as you want to login'
    mocked_print.assert_any_call('-*-' * len(line))
    mocked_print.assert_any_call(line)


# TODO: test different menus for student/teacher/admin
# TODO: test http requests
