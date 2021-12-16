import json

import requests
from dataclasses import dataclass
from typeguard import typechecked

from domain_objects.user import Student, User
from domain_objects.lesson import Lesson
from validation.dataclasses import validate_dataclass

API_SERVER_ADDRESS = 'http://localhost:8000/api/v1'


#@typechecked
@dataclass(frozen=True)
class Handler:
    user: User

    def __post_init__(self):
        validate_dataclass(self)

    def fetch_lessons(self):
        headers = {'Content-Type': 'application/json',
                   'Authorization': "Token " + self.user.token}
        response = requests.get(
            f'{API_SERVER_ADDRESS}/lessons/', headers=headers)
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
        payload = {
            'name': lesson.lesson_name,
            "instrument": lesson.instrument.as_json(),
            "teacher": self.user.as_json(),
            'date_time': lesson.date_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'duration': str(lesson.duration),
            'cost': str(lesson.cost),
        }
        headers = {'Content-Type': 'application/json',
                   'Authorization': "Token " + self.user.token}
        response = requests.post(
            url=f'{API_SERVER_ADDRESS}/lessons/', json=payload, headers=headers)
        print("Url ", response.request.url)

        print("Body ", response.request.body)
        print("-" * 50)
        print(response.content)
        if not (response.status_code == 200 or response.status_code == 204):
            return False
        return True

    def modify_lesson(self, lesson: Lesson):
        payload = {
            'name': lesson.lesson_name,
            'instrument': lesson.instrument,
            'teacher': lesson.teacher,
            'date_time': lesson.date_time,
            'duration': lesson.duration,
            'cost': lesson.cost,
            'Token': self.user.token,
        }
        # TODO: check url w.r.t the backend
        response = requests.put(f'{API_SERVER_ADDRESS}/lessons', data=payload)
        if not (response.status_code == 200 or response.status_code == 204):
            return False
        return True

    def cancel_lesson(self, lesson_id: str):
        headers = {'Authorization': "Token " + self.user.token}
        # TODO: check url w.r.t the backend
        response = requests.delete(
            f'{API_SERVER_ADDRESS}/lessons/'+lesson_id, headers=headers)
        print(response.status_code)
        if not (response.status_code == 200 or response.status_code == 204):
            return False
        return True

    def fetch_booking(self):
        headers = {'Authorization': "Token " + self.user.token}
        response = requests.get(
            f'{API_SERVER_ADDRESS}/booking/', headers=headers)
        if response.status_code != 200:
            return None
        return response.json()

    def book_lesson(self, lesson_name: str):
        payload = {'name': lesson_name, 'Token': self.user.token}
        response = requests.post(
            f'{API_SERVER_ADDRESS}/booking/', data=payload)
        if response.status_code != 200:
            return False
        return True

    def cancel_booking(self, lesson_id: str):
        headers = {'Authorization': "Token " + self.user.token}
        response = requests.delete(
            f'{API_SERVER_ADDRESS}/booking/'+lesson_id, headers=headers)
        if not (response.status_code == 200 or response.status_code == 204):
            return False
        return True
