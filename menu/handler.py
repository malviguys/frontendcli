import requests
from domain_objects.user import Student, User
from domain_objects.lesson import Lesson


API_SERVER_ADDRESS = 'http://localhost:8000/api/v1'

class Handler:
    __user: User

    @property
    def user(self) -> User:
        return self.__user


    def fetch_lessons(self):
        payload = {'Token':self.__handler.user.token}
        # TODO: check url
        response = requests.get(f'{API_SERVER_ADDRESS}/lessons', params = payload)
        if response.status_code != 200:
            return None
        return response.json()

    def create_lesson(self, lesson:Lesson):
        if isinstance(self.__user, Student):
            return
        # Validate lesson ?
        payload = {
            'name': lesson.lesson_name,
            'instrument': lesson.instrument,
            'teacher': lesson.teacher,
            'date_time': lesson.date_time,
            'duration': lesson.duration,
            'cost': lesson.cost,
        }
        # TODO: check url
        response = requests.post(f'{API_SERVER_ADDRESS}/lessons', data = payload)
    
    def modify_lesson(self, lesson:Lesson):
        if isinstance(self.__user, Student):
            return
        
        payload = {
            'name': lesson.lesson_name,
            'instrument': lesson.instrument,
            'teacher': lesson.teacher,
            'date_time': lesson.date_time,
            'duration': lesson.duration,
            'cost': lesson.cost,
        }
        # TODO: check url
        response = requests.put(f'{API_SERVER_ADDRESS}/lessons', data = payload)

    def cancel_lesson(self, lesson_name:str):
        if isinstance(self.__user, Student):
            return
        payload = {'name': lesson_name}
        # TODO: check url
        response = requests.delete(f'{API_SERVER_ADDRESS}/lessons', params = payload)

	
    def book_lesson(self, lesson_name: str):
        payload = {'name': lesson_name}
        # TODO: check url
        response = requests.post(f'{API_SERVER_ADDRESS}/booking/', data = payload)
	
    def cancel_booking(self, lesson_name: str):
        payload = {'name': lesson_name}
        # TODO: check url
        response = requests.delete(f'{API_SERVER_ADDRESS}/booking/', params = payload)

