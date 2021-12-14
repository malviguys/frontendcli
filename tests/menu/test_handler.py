import datetime
from http.client import responses

import responses
import pytest

from domain_objects.cost import Cost
from domain_objects.lesson import Lesson, Instrument
from domain_objects.user import User, Student, Username
from menu.handler import Handler, API_SERVER_ADDRESS

ENDPOINT_PRE = "/api/v1"


@pytest.fixture()
def handler():
    return Handler(User.create('FancyUsername', 'SecretToken'))


@pytest.fixture()
def student_handler():
    return Handler(Student(Username('Student'), 'StudentToken'))  # TODO: change Username to be able to take string


@pytest.fixture()
def lesson():
    lesson_name = 'SSD'
    teacher = 'Mario Alviano'
    instrument = Instrument.TRIANGLE
    students = []
    date_time = datetime.datetime(year=2022, month=12, day=16, hour=14, minute=30)
    duration = datetime.timedelta(hours=2)
    cost = Cost.parse('150.00')
    return Lesson.create(lesson_name, teacher, instrument, students, date_time, duration, cost)


def test_create_handler():
    handler = Handler(User.create('Momo', 'abcde456'))
    assert str(handler.user.username) == 'Momo' and handler.user.token == 'abcde456'


def test_cannot_create_handler_without_user():
    with pytest.raises(TypeError):
        Handler()


@responses.activate
def test_fetch_lessons_200(handler):
    responses.add(**{
        'method': responses.GET,
        'url': API_SERVER_ADDRESS + '/lessons',
        'body': '{"OK": "Working fine"}',
        'status': 200,
        'content_type': 'application/json',
    })
    assert str(handler.fetch_lessons()) == "{'OK': 'Working fine'}"


@responses.activate
def test_fetch_lessons_fails(handler):
    responses.add(**{
        'method': responses.GET,
        'url': API_SERVER_ADDRESS + '/lessons',
        'body': '{"UNAUTHORIZED": "You are not allowed to see this content"}',
        'status': 401,
        'content_type': 'application/json',
    })
    assert handler.fetch_lessons() is None


@responses.activate
def test_create_lesson(handler, lesson):
    responses.add(**{
        'method': responses.POST,
        'url': API_SERVER_ADDRESS + '/lessons',
        'body': '{"CREATED": "Congrats! A new lesson!"}',
        'status': 204,
        'content_type': 'application/json',
    })
    assert handler.create_lesson(lesson) is True


@responses.activate
def test_create_lesson_fails(handler, lesson):
    responses.add(**{
        'method': responses.POST,
        'url': API_SERVER_ADDRESS + '/lessons',
        'body': '{"UNAUTHORIZED": "You can\'t do nothing"}',
        'status': 401,
        'content_type': 'application/json',
    })
    assert handler.create_lesson(lesson) is False


def test_create_lesson_fails_student(student_handler, lesson):
    assert student_handler.create_lesson(lesson) is False


@responses.activate
def test_modify_lesson(handler, lesson):
    responses.add(**{
        'method': responses.PUT,
        'url': API_SERVER_ADDRESS + '/lessons',
        'body': '{"OK": "Made changes"}',
        'status': 200,
        'content_type': 'application/json',
    })
    assert handler.modify_lesson(lesson) is True


@responses.activate
def test_modify_lesson_fails(handler, lesson):
    responses.add(**{
        'method': responses.PUT,
        'url': API_SERVER_ADDRESS + '/lessons',
        'body': '{"UNAUTHORIZED": "Can\'t touch this"}',
        'status': 401,
        'content_type': 'application/json',
    })
    assert handler.modify_lesson(lesson) is False


def test_modify_lesson_fails_student(student_handler, lesson):
    assert student_handler.modify_lesson(lesson) is False


@responses.activate
def test_cancel_lesson(handler, lesson):
    responses.add(**{
        'method': responses.DELETE,
        'url': API_SERVER_ADDRESS + '/lessons',
        'body': '{"OK": "Put into the bin"}',
        'status': 200,
        'content_type': 'application/json',
    })
    assert handler.cancel_lesson(lesson.lesson_name) is True


@responses.activate
def test_cancel_lesson_fails(handler, lesson):
    responses.add(**{
        'method': responses.DELETE,
        'url': API_SERVER_ADDRESS + '/lessons',
        'body': '{"UNAUTHORIZED": "Don\'t you dare messing with admin stuff"}',
        'status': 401,
        'content_type': 'application/json',
    })
    assert handler.cancel_lesson(lesson.lesson_name) is False


def test_cancel_lesson_fails_student(student_handler, lesson):
    assert student_handler.cancel_lesson(lesson.lesson_name) is False


@responses.activate
def test_book_lesson(handler, lesson):
    responses.add(**{
        'method': responses.POST,
        'url': API_SERVER_ADDRESS + '/booking/',
        'body': '{"OK": "You are accepted"}',
        'status': 200,
        'content_type': 'application/json',
    })
    assert handler.book_lesson(lesson.lesson_name) is True


@responses.activate
def test_book_lesson_fails(handler, lesson):
    responses.add(**{
        'method': responses.POST,
        'url': API_SERVER_ADDRESS + '/booking/',
        'body': '{"UNAUTHORIZED": "You are not allowed to educate!"}',
        'status': 401,
        'content_type': 'application/json',
    })
    assert handler.book_lesson(lesson.lesson_name) is False


@responses.activate
def test_cancel_booking(handler, lesson):
    responses.add(**{
        'method': responses.DELETE,
        'url': API_SERVER_ADDRESS + '/booking/',
        'body': '{"OK": "You are free"}',
        'status': 200,
        'content_type': 'application/json',
    })
    assert handler.cancel_booking(lesson.lesson_name) is True


@responses.activate
def test_cancel_booking_fails(handler, lesson):
    responses.add(**{
        'method': responses.DELETE,
        'url': API_SERVER_ADDRESS + '/booking/',
        'body': '{"UNAUTHORIZED": "You chose - you must attend!"}',
        'status': 401,
        'content_type': 'application/json',
    })
    assert handler.cancel_booking(lesson.lesson_name) is False

