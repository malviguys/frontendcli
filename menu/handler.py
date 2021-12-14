import json

import requests
from attr import dataclass
from typeguard import typechecked

from domain_objects.user import Student, User
from domain_objects.lesson import Lesson
from validation.dataclasses import validate_dataclass

API_SERVER_ADDRESS = 'http://localhost:8000/api/v1'


@typechecked
@dataclass(frozen=True)
class Handler:
    user: User

    def __post_init__(self):
        validate_dataclass(self)

    def fetch_lessons(self):
        payload = {'Token': self.user.token}
        # TODO: check url
        response = requests.get(f'{API_SERVER_ADDRESS}/lessons', params=payload)
        if response.status_code != 200:
            return None
        return response.json()
        # return json.loads('{"lessons": [{"id":1, "lesson_name":"Guitar With Mario", "teacher":"Mario Alviano", '
        #                   '"instrument":"Instrument.GUITAR", "students":[{"name":"Claudio Lucisano"}, {"name":"Giada Gabriele"}], '
        #                   '"date_time":"2021-16-12 14:30:00", "duration":"00:02:00", "cost":"100.00€"},'
        #                   '{"id":2, "lesson_name":"Fun with the Triangle", "teacher":"Dr. Tri Angle", '
        #                   '"instrument":"Instrument.TRIANGLE", "students":[{"name":"Paola Guarasci"}, {"name":"Kerstin Greifensteiner"}], '
        #                   '"date_time":"2021-17-02 12:30:00", "duration":"00:03:30", "cost":"120.00€"}]}')

    def create_lesson(self, lesson: Lesson):
        if isinstance(self.user, Student):
            return False
        payload = {
            'name': lesson.lesson_name,
            'instrument': lesson.instrument,
            'teacher': lesson.teacher,
            'date_time': lesson.date_time,
            'duration': lesson.duration,
            'cost': lesson.cost,
        }
        # TODO: check url
        response = requests.post(f'{API_SERVER_ADDRESS}/lessons', data=payload)
        if not (response.status_code == 200 or response.status_code == 204):
            return False
        return True

    def modify_lesson(self, lesson: Lesson):
        if isinstance(self.user, Student):
            return False

        payload = {
            'name': lesson.lesson_name,
            'instrument': lesson.instrument,
            'teacher': lesson.teacher,
            'date_time': lesson.date_time,
            'duration': lesson.duration,
            'cost': lesson.cost,
        }
        # TODO: check url
        response = requests.put(f'{API_SERVER_ADDRESS}/lessons', data=payload)
        if not (response.status_code == 200 or response.status_code == 204):
            return False
        return True

    def cancel_lesson(self, lesson_name: str):
        if isinstance(self.user, Student):
            return False
        payload = {'name': lesson_name}
        # TODO: check url
        response = requests.delete(f'{API_SERVER_ADDRESS}/lessons', params=payload)
        if not (response.status_code == 200 or response.status_code == 204):
            return False
        return True

    def book_lesson(self, lesson_name: str):
        payload = {'name': lesson_name}
        # TODO: check url
        response = requests.post(f'{API_SERVER_ADDRESS}/booking/', data=payload)
        if response.status_code != 200:
            return False
        return True

    def cancel_booking(self, lesson_name: str):
        payload = {'name': lesson_name}
        # TODO: check url
        response = requests.delete(f'{API_SERVER_ADDRESS}/booking/', params=payload)
        if not (response.status_code == 200 or response.status_code == 204):
            return False
        return True
