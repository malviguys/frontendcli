import pytest
import datetime
from valid8 import ValidationError

from core.domain_objects.cost import Cost
from core.domain_objects.lesson import Lesson, Instrument


@pytest.fixture
def lesson():
    lesson_name = 'SSD'
    teacher = 'Mario Alviano'
    instrument = Instrument.TRIANGLE
    students = []
    date_time = datetime.datetime(year=2022, month=12, day=16, hour=14, minute=30)
    duration = datetime.timedelta(hours=2)
    cost = Cost.parse('150.00')
    return Lesson.create(lesson_name, teacher, instrument, students, date_time, duration, cost)


def test_create_lesson_name_fails_starts_with_digit(lesson):
    failing_name = '3DoesNotStartWithLetter'
    with pytest.raises(ValidationError):
        Lesson.create(failing_name, lesson.teacher, lesson.instrument, lesson.students,
                      lesson.date_time, lesson.duration, lesson.cost)


def test_create_lesson_name_fails_too_long(lesson):
    failing_name = 'A'*81
    with pytest.raises(ValidationError):
        Lesson.create(failing_name, lesson.teacher, lesson.instrument, lesson.students,
                      lesson.date_time, lesson.duration, lesson.cost)


def test_create_lesson_name_fails_too_short(lesson):
    failing_name = 'A'
    with pytest.raises(ValidationError):
        Lesson.create(failing_name, lesson.teacher, lesson.instrument, lesson.students,
                      lesson.date_time, lesson.duration, lesson.cost)


def test_create_lesson_name_fails_invalid_characters(lesson):
    for special_char in ['\nab', '\rab', '*ab', '^ab', '$ab', '€ab', '@ab']:
        with pytest.raises(ValidationError):
            Lesson.create(special_char, lesson.teacher, lesson.instrument, lesson.students,
                          lesson.date_time, lesson.duration, lesson.cost)


def test_create_lesson_teacher_fails_too_long(lesson):
    failing_teacher = 'Mario A' + 'a'*74
    print(failing_teacher)
    with pytest.raises(ValidationError):
        Lesson.create(lesson.lesson_name, failing_teacher, lesson.instrument, lesson.students,
                      lesson.date_time, lesson.duration, lesson.cost)


def test_create_lesson_teacher_fails_too_short(lesson):
    failing_teacher = 'H'
    with pytest.raises(ValidationError):
        Lesson.create(lesson.lesson_name, failing_teacher, lesson.instrument, lesson.students,
                      lesson.date_time, lesson.duration, lesson.cost)


def test_create_lesson_teacher_fails_no_last_name(lesson):
    failing_teacher = 'Mario'
    with pytest.raises(ValidationError):
        Lesson.create(lesson.lesson_name, failing_teacher, lesson.instrument, lesson.students,
                      lesson.date_time, lesson.duration, lesson.cost)


def test_create_lesson_teacher_fails_only_title(lesson):
    failing_teacher = 'Dr.'
    with pytest.raises(ValidationError):
        Lesson.create(lesson.lesson_name, failing_teacher, lesson.instrument, lesson.students,
                      lesson.date_time, lesson.duration, lesson.cost)


def test_create_lesson_fails_illegal_characters(lesson):
    for special_char in ['\nImma Teacher', 'Abc\r Def', 'St*r Dancer', 'Hold^ On', 'T$ll Me Why', '€uro Picker', 'Email @Address']:
        with pytest.raises(ValidationError):
            Lesson.create(lesson.lesson_name, special_char, lesson.instrument, lesson.students,
                          lesson.date_time, lesson.duration, lesson.cost)


def test_create_lesson_fails_datetime_in_past(lesson):
    failing_date_time = datetime.datetime(year=2020, month=12, day=16, hour=14, minute=30)
    with pytest.raises(ValueError):
        Lesson.create(lesson.lesson_name, lesson.teacher, lesson.instrument, lesson.students,
                      failing_date_time, lesson.duration, lesson.cost)


def test_create_lesson_fails_datetime_too_far_in_future(lesson):
    failing_date_time = datetime.datetime(year=2025, month=12, day=16, hour=14, minute=30)
    with pytest.raises(ValueError):
        Lesson.create(lesson.lesson_name, lesson.teacher, lesson.instrument, lesson.students,
                      failing_date_time, lesson.duration, lesson.cost)


def test_create_lesson_duration_fails_too_long(lesson):
    failing_duration = datetime.timedelta(hours=5)
    with pytest.raises(ValueError):
        Lesson.create(lesson.lesson_name, lesson.teacher, lesson.instrument, lesson.students,
                      lesson.date_time, failing_duration, lesson.cost)


def test_create_lesson_duration_fails_too_short(lesson):
    failing_duration = datetime.timedelta(minutes=30)
    with pytest.raises(ValueError):
        Lesson.create(lesson.lesson_name, lesson.teacher, lesson.instrument, lesson.students,
                      lesson.date_time, failing_duration, lesson.cost)


def test_lesson_string():
    lesson_name = "Drums 101"
    teacher = "Mario Alviano"
    instrument = Instrument.DRUM
    students = []
    date_time = datetime.datetime(year=2022, month=6, day=16, hour=14, minute=30)
    duration = datetime.timedelta(hours=3)
    cost = Cost.create(220, 80)
    expected_string = f'Lesson {lesson_name}: \n\tPresented By: {teacher} \n\tInstrument: {instrument.name} ' \
                        f'\n\tScheduled At: {date_time} \n\tDuration: {duration} hours \n\tCost: {cost.__str__()}€ ' \
                        f'\n\tRegistered Students: {students}'
    assert str(Lesson.create(lesson_name, teacher, instrument, students, date_time, duration, cost)) == expected_string
