import pytest
import datetime
from valid8 import ValidationError

from domain_objects.cost import Cost
from domain_objects.lesson import Lesson, Instrument


@pytest.fixture
def lesson():
    lesson_name = 'SSD'
    teacher = 'Mario Alviano'
    instrument = Instrument.TRIANGLE
    students = []
    date_time = datetime.datetime(year=2021, month=12, day=16, hour=14, minute=30)
    duration = datetime.timedelta(hours=2)
    cost = Cost.parse('150.00')
    return Lesson.create(lesson_name, teacher, instrument, students, date_time, duration, cost)


def test_create_lesson_valid_name(lesson):
    lesson_name = 'Very-LongLessonNameForTestingPurposes 42'
    l = Lesson.create(lesson_name, lesson.teacher, lesson.instrument, lesson.students,
                      lesson.date_time, lesson.duration, lesson.cost)
    assert l.lesson_name == lesson_name


def test_create_lesson_name_fails_starts_with_digit(lesson):
    failing_name = '3DoesNotStartWithLetter'
    with pytest.raises(ValidationError):
        Lesson.create(failing_name, lesson.teacher, lesson.instrument, lesson.students,
                      lesson.date_time, lesson.duration, lesson.cost)


def test_create_lesson_name_fails_too_long(lesson):
    failing_name = 'ThisIsAVeryLongLessonNameThatShouldFail42'
    with pytest.raises(ValidationError):
        Lesson.create(failing_name, lesson.teacher, lesson.instrument, lesson.students,
                      lesson.date_time, lesson.duration, lesson.cost)


def test_create_lesson_name_fails_too_short(lesson):
    failing_name = 'A'
    with pytest.raises(ValidationError):
        Lesson.create(failing_name, lesson.teacher, lesson.instrument, lesson.students,
                      lesson.date_time, lesson.duration, lesson.cost)


def test_create_lesson_name_fails_wrong_characters(lesson):
    failing_name = '€häractersNot@llöwed'
    with pytest.raises(ValidationError):
        Lesson.create(failing_name, lesson.teacher, lesson.instrument, lesson.students,
                      lesson.date_time, lesson.duration, lesson.cost)

