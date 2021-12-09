import requests

from domain_objects.lesson import Lesson
from domain_objects.user import Admin, Student, User

class Menu():
	__API_SERVER_ADDRESS = ''

	def fetch_lessons(self, user:User):
		response = requests.get(url=f'{self.__API_SERVER_ADDRESS}/lessons')
		if response.status_code != 200:
			return None
		return response.json()

	def book_lesson(self, lesson:Lesson, user:Student):
		payload = {'name':lesson.lesson_name}

	def create_lesson(self, lesson:Lesson, user:Admin):
		pass

	def cancel_lesson(self, lesson:Lesson, user:Admin):
		pass

	def modify_lesson(self, lesson:Lesson, user:Admin):
		pass

