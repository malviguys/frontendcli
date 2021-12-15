import json
from unittest.mock import patch, Mock, mock_open

import pytest
import requests
import responses

from core.app import App
from menu.handler import Handler, API_SERVER_ADDRESS


def test_create_app():
    App()


@patch('builtins.print')
def test_app_asks_for_login(mocked_print):
    App().run()
    line = 'Please, select as you want to login'
    mocked_print.assert_any_call('-*-' * len(line))
    mocked_print.assert_any_call(line)


@pytest.fixture
def mock_fetch_lessons():
    Handler.fetch_lessons = Mock()
    Handler.fetch_lessons.return_value = json.loads('{"lessons": [{"id":1, "lesson_name":"Guitar With Mario", '
                                                    '"teacher":"Mario Alviano", "instrument":"Instrument.GUITAR", '
                                                    '"students":[{"name":"Claudio Lucisano"}, {"name":"Giada Gabriele"}], '
                                                    '"date_time":"2021-16-12 14:30:00", "duration":"00:02:00", "cost":"100.00€"},'
                                                    '{"id":2, "lesson_name":"Fun with the Triangle", "teacher":"Dr. Tri Angle", '
                                                    '"instrument":"Instrument.TRIANGLE", "students":[{"name":"Paola Guarasci"}, '
                                                    '{"name":"Kerstin Greifensteiner"}], "date_time":"2021-17-02 12:30:00", '
                                                    '"duration":"00:03:30", "cost":"120.00€"}]}')
    return Handler


@pytest.fixture
def mock_create_lesson():
    Handler.create_lesson = Mock()
    Handler.create_lesson.return_value = True
    return Handler


@responses.activate
@patch('builtins.input', side_effect=['1', 'student', 'mypassword', '0'])
@patch('builtins.print')
def test_student_login(mocked_print, mocked_input):
    responses.add(**{
        'method': responses.POST,
        'url': API_SERVER_ADDRESS + '/auth/login/',
        'body': '{"key": "You are in"}',
        'status': 200,
        'content_type': 'application/json',
    })

    with patch.object(Handler, 'fetch_lessons'):
        with patch('builtins.open', mock_open()):
            App().run()
            mocked_print.assert_any_call('1-\tLog in as a Student')
            mocked_print.assert_any_call('2-\tLog in as a Teacher')
            mocked_print.assert_any_call('3-\tLog in as an Admin')
            mocked_print.assert_any_call('0-\tExit')
            mocked_print.assert_any_call('Logging as a Student')
            mocked_print.assert_any_call('Successfully logged in!\n')
            mocked_print.assert_any_call('1-\tBook a lesson')
            mocked_print.assert_any_call('2-\tCancel a booking')
            mocked_print.assert_any_call('0-\tExit')
            mocked_print.assert_any_call('Goodbye fella')
            mocked_input.assert_called()


@responses.activate
@patch('builtins.input', side_effect=['2', 'teacher', 'myfancypassword', '0'])
@patch('builtins.print')
def test_teacher_login(mocked_print, mocked_input):
    responses.add(**{
        'method': responses.POST,
        'url': API_SERVER_ADDRESS + '/auth/login/',
        'body': '{"key": "You are in"}',
        'status': 200,
        'content_type': 'application/json',
    })
    with patch.object(Handler, 'fetch_lessons'):
        with patch('builtins.open', mock_open()):
            App().run()
            mocked_print.assert_any_call('1-\tLog in as a Student')
            mocked_print.assert_any_call('2-\tLog in as a Teacher')
            mocked_print.assert_any_call('3-\tLog in as an Admin')
            mocked_print.assert_any_call('0-\tExit')
            mocked_print.assert_any_call('Logging as a Teacher')
            mocked_print.assert_any_call('Successfully logged in!\n')
            mocked_print.assert_any_call('1-\tCreate a lesson')
            mocked_print.assert_any_call('2-\tModify a lesson')
            mocked_print.assert_any_call('3-\tCancel a lesson')
            mocked_print.assert_any_call('0-\tExit')
            mocked_print.assert_any_call('Goodbye fella')
            mocked_input.assert_called()


@responses.activate
@patch('builtins.input', side_effect=['3', 'admin', 'admin', '0'])
@patch('builtins.print')
def test_admin_login(mocked_print, mocked_input):
    # TODO: duplicate
    responses.add(**{
        'method': responses.POST,
        'url': API_SERVER_ADDRESS + '/auth/login/',
        'body': '{"key": "You are in"}',
        'status': 200,
        'content_type': 'application/json',
    })
    with patch.object(Handler, 'fetch_lessons'):
        with patch('builtins.open', mock_open()):
            App().run()
            mocked_print.assert_any_call('1-\tLog in as a Student')
            mocked_print.assert_any_call('2-\tLog in as a Teacher')
            mocked_print.assert_any_call('3-\tLog in as an Admin')
            mocked_print.assert_any_call('0-\tExit')
            mocked_print.assert_any_call('Logging as an Admin')
            mocked_print.assert_any_call('Successfully logged in!\n')
            mocked_print.assert_any_call('1-\tCreate a lesson')
            mocked_print.assert_any_call('2-\tModify a lesson')
            mocked_print.assert_any_call('3-\tCancel a lesson')
            mocked_print.assert_any_call('4-\tGet admin page link')
            mocked_print.assert_any_call('0-\tExit')
            mocked_print.assert_any_call('Goodbye fella')
            mocked_input.assert_called()


@responses.activate
@patch('builtins.input', side_effect=['2', 'teacher', 'tchr', '1',
                                      'My Lesson', 'Guitar', 'Myself Thatsit', '08-03-2022 10:00', '120', '80.00', '0'])
@patch('builtins.print')
def test_create_lesson(mocked_print, mocked_input):
    responses.add(**{
        'method': responses.POST,
        'url': API_SERVER_ADDRESS + '/auth/login/',
        'body': '{"key": "You are in"}',
        'status': 200,
        'content_type': 'application/json',
    })
    with patch.object(Handler, 'create_lesson'):
        with patch('builtins.open', mock_open()):
            App().run()
            mocked_print.assert_any_call(f'Lesson "My Lesson" with Myself Thatsit for Guitar on 2022-03-08 10:00:00 '
                                         f'for 2.0 hours and 80.00€ created successfully!\n')
            mocked_print.assert_any_call('Goodbye fella')
            mocked_input.assert_called()


@responses.activate
@patch('builtins.input', side_effect=['2', 'teacher', 'tchr', '1',
                                      'My Lesson', 'Guitar', 'Myself Thatsit', '08-03-2022 10:00', '120', '80.00', '0'])
@patch('builtins.print')
def test_create_lesson_fails_from_backend(mocked_print, mocked_input):
    responses.add(**{
        'method': responses.POST,
        'url': API_SERVER_ADDRESS + '/auth/login/',
        'body': '{"key": "You are in"}',
        'status': 200,
        'content_type': 'application/json',
    })
    with patch.object(Handler, 'create_lesson') as mocked_create_lesson:
        mocked_create_lesson.return_value = False
        with patch('builtins.open', mock_open()):
            App().run()
            mocked_print.assert_any_call('The lesson could not be created!\n')
            mocked_print.assert_any_call('Goodbye fella')
            mocked_input.assert_called()


