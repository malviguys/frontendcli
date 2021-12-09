from dataclasses import dataclass


@dataclass(frozen=True)
class User:
	is_admin:bool

	def login(self):
		pass

	def logout(self):
		pass


class Student(User):
	def book_lesson():
		pass


class Admin(User):
	# TODO: What if the admin is redirected to the django admin page?
	def create_lesson():
		pass