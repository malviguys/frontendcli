import datetime
import requests
from typeguard import typechecked
from domain_objects.lesson import Lesson
from domain_objects.user import Admin, Student, Teacher, User, Username
from menu.handler import Handler
from menu.menu import API_SERVER_ADDRESS, Description, Entry, Menu

ADMIN_PAGE = ''

class App:
    __menu: Menu
    __handler: Handler

    __app_name = 'Welcome to MusiLesson 0.1!'
    __insert_username_field = 'Insert your username:'
    __insert_password_field = 'Insert your password:'
    __salut = 'Goodbye fella'

    def __init__(self):
        def ask_to_login():
            line = 'Please, select as you want to login'
            print('-*-'*len(line))
            print(line)
            print('-*-'*len(line))

        self.__login_menu = Menu.Builder(Description(self.__app_name), auto_select=lambda: ask_to_login())\
            .with_entry(Entry.create('1', 'Log in as a Student', on_selected = lambda: self.__do_login_as_student()))\
            .with_entry(Entry.create('2', 'Log in as a Teacher', on_selected = lambda: self.__do_login_as_teacher()))\
            .with_entry(Entry.create('3', 'Log in as an Admin', on_selected = lambda: self.__do_login_as_admin()))\
            .with_entry(Entry.create('0', 'Exit', on_selected = lambda: print(self.__salut), is_exit = True))\
            .build()
    
    @typechecked
    def __do_login_as_student(self) -> 'Student':
        print('Logging as a Student')

        user_name = input(self.__insert_username_field)
        pwd = input(self.__insert_password_field)

        payload = dict(username=user_name, password=pwd)
        response = requests.post(f'{API_SERVER_ADDRESS}/auth/login/', data = payload)

        # TODO: check if the key is taken correctly
        user = Student(Username(user_name), response.json()['key'])

        self.__handler = Handler(user)

        self.__menu = Menu.Builder(Description(self.__app_name), auto_select=lambda: self.__print_lessons())\
            .with_entry(Entry.create('1', 'Book a lesson', on_selected = lambda: self.__book_lesson()))\
            .with_entry(Entry.create('2', 'Cancel a booking', on_selected = lambda: self.__cancel_booking()))\
            .with_entry(Entry.create('0', 'Exit', on_selected = lambda: print(self.__salut), is_exit = True))\
            .build()

    @typechecked
    def __do_login_as_teacher(self) -> 'Teacher':
        print('Logging as a Teacher')

        user_name = input(self.__insert_username_field)
        pwd = input(self.__insert_password_field)

        payload = dict(username=user_name, password=pwd)
        response = requests.post(f'{API_SERVER_ADDRESS}/auth/login/', data = payload)

        # TODO: check if the key is taken correctly
        user = Teacher(Username(user_name), response.json()['key'])

        self.__handler = Handler(user)

        self.__menu = Menu.Builder(Description(self.__app_name), auto_select=lambda: self.__print_lessons())\
            .with_entry(Entry.create('1', 'Create a lesson', on_selected = lambda: self.__create_lesson()))\
            .with_entry(Entry.create('2', 'Modify a lesson', on_selected = lambda: self.__modify_lesson()))\
            .with_entry(Entry.create('3', 'Cancel a lesson', on_selected = lambda: self.__cancel_lesson()))\
            .with_entry(Entry.create('0', 'Exit', on_selected = lambda: print(self.__salut), is_exit = True))\
            .build()

    @typechecked
    def __do_login_as_admin(self) -> 'Admin':
        print('Logging as an Admin')

        user_name = input(self.__insert_username_field)
        pwd = input(self.__insert_password_field)

        payload = dict(username=user_name, password=pwd)
        response = requests.post(f'{API_SERVER_ADDRESS}/auth/login/', data = payload)

        # TODO: check if the key is taken correctly
        user = Admin(Username(user_name), response.json()['key'])
        
        self.__handler = Handler(user)

        # TODO: Discuss on wether the `get admin page link` is useful
        self.__menu = Menu.Builder(Description(), auto_select=lambda: self.__print_lessons())\
            .with_entry(Entry.create('1', 'Create a lesson', on_selected = lambda: self.__create_lesson()))\
            .with_entry(Entry.create('2', 'Modify a lesson', on_selected = lambda: self.__modify_lesson()))\
            .with_entry(Entry.create('3', 'Cancel a lesson', on_selected = lambda: self.__cancel_lesson()))\
            .with_entry(Entry.create('4', 'Get admin page link', on_selected = lambda: self.__get_admin_page()))\
            .with_entry(Entry.create('0', 'Exit', on_selected = lambda: print(self.__salut), is_exit = True))\
            .build()

    def __print_lessons(self) -> None:
        # TODO: do a better format
        lessons_json = self.__handler.fetch_lessons()
        print (lessons_json)
    
    def __create_lesson(self):
        name = input("Insert the name of the lesson:")
        instrument = input("Insert the instrument that'll be studied:")
        teacher = input("Insert the teacher of the lesson:")
        user_dt_input = input("Insert the date and the time of the lesson: ~ format: {DD-MM-YYYY hh:mm} ~")
        date_split = user_dt_input.split(' ')[0]
        time_split = user_dt_input.split(' ')[1]
        date_time = datetime.datetime(day = date_split.split('-')[0], month = date_split.split('-')[1], year = date_split.split('-')[2], hour = time_split.split(':')[0], minute = time_split.split(':')[1])
        duration = datetime.timedelta(minutes = input("Insert the duration (in minutes) of the lesson:"))
        cost = input("Insert the cost of the lesson")
        lesson = Lesson.create(name, teacher, instrument, date_time, duration, cost)

        self.__handler.create_lesson(lesson)
    
    def __modify_lesson(self):
        name = input("Insert the name of the lesson:")
        instrument = input("Insert the instrument that'll be studied:")
        teacher = input("Insert the teacher of the lesson:")
        user_dt_input = input("Insert the date and the time of the lesson: ~ format: {DD-MM-YYYY hh:mm} ~")
        date_split = user_dt_input.split(' ')[0]
        time_split = user_dt_input.split(' ')[1]
        date_time = datetime.datetime(day = date_split.split('-')[0], month = date_split.split('-')[1], year = date_split.split('-')[2], hour = time_split.split(':')[0], minute = time_split.split(':')[1])
        duration = datetime.timedelta(minutes = input("Insert the duration (in minutes) of the lesson:"))
        cost = input("Insert the cost of the lesson")
        lesson = Lesson.create(name, teacher, instrument, date_time, duration, cost)

        self.__handler.modify_lesson(lesson)
    
    def __cancel_lesson(self):
        lesson_name = input("Insert the name of the lesson to delete:")
        self.__handler.cancel_lesson(lesson_name)
    
    def __book_lesson(self) -> None:
        lesson_name = input("Insert the name of the lesson to book for:")
        self.__handler.book_lesson(lesson_name)
    
    def __cancel_booking(self):
        lesson_name = input("Insert the name of the lesson to delete the reservation:")
        self.__handler.cancel_booking(lesson_name)

    def __get_admin_page(self):
        print(f'Admin page: {ADMIN_PAGE}')

    def __run(self) -> None:
        self.__login_menu.run()
        self.__menu.run()

    def run(self) -> None:
        try:
            self.__run()
        except Exception:
            print('Something went horribly wrong.')



def main():
    App().run()

if __name__ == "__main__":
    main()