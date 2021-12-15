import datetime
from traceback import print_exc

import requests
from typeguard import typechecked

from domain_objects.cost import Cost
from domain_objects.lesson import Lesson, Instrument
from domain_objects.user import Admin, Student, Teacher, User, Username
from menu.handler import Handler, API_SERVER_ADDRESS
from menu.menu import Description, Entry, Menu

ADMIN_PAGE = ''

def do_login():
    while True:
        user_name = input('Insert your username:')
        pwd = input('Insert your password:')

        payload = dict(username=user_name, password=pwd)
        
        response = requests.post(f'{API_SERVER_ADDRESS}/auth/login/', data=payload)

        if response.status_code != requests.codes.ok:
            print("Invalid credential, please try again.")
            continue
        
        token = response.json()['key']
        return user_name, token


def __setup_lesson():
        name = input("Insert the name of the lesson:")
        instrument = input("Insert the instrument that'll be studied:")
        teacher = input("Insert the teacher of the lesson:")
        user_dt_input = input("Insert the date and the time of the lesson: ~ format: {DD-MM-YYYY hh:mm} ~")
        date_split = user_dt_input.split(' ')[0]
        time_split = user_dt_input.split(' ')[1]
        date_time = datetime.datetime(day=int(date_split.split('-')[0]), month=int(date_split.split('-')[1]),
                                      year=int(date_split.split('-')[2]), hour=int(time_split.split(':')[0]),
                                      minute=int(time_split.split(':')[1]))
        duration = datetime.timedelta(minutes=int(input("Insert the duration (in minutes) of the lesson:")))
        cost = input("Insert the cost of the lesson")
        return Lesson.create(name, teacher, instrument, date_time, duration, cost)


class App:
    __menu: Menu
    __handler: Handler

    __app_name = 'Welcome to MusiLesson'  # Description does not allow '.' or '!'
    __salut = 'Goodbye fella'

    def __init__(self):
        def ask_to_login():
            line = 'Please, select as you want to login'
            print('-*-' * len(line))
            print(line)
            print('-*-' * len(line))

        self.__login_menu = Menu.Builder(Description(self.__app_name), auto_select=lambda: ask_to_login()) \
            .with_entry(Entry.create('1', 'Log in as a Student', on_selected=lambda: self.__do_login_as_student(), is_exit=True)) \
            .with_entry(Entry.create('2', 'Log in as a Teacher', on_selected=lambda: self.__do_login_as_teacher(), is_exit=True)) \
            .with_entry(Entry.create('3', 'Log in as an Admin', on_selected=lambda: self.__do_login_as_admin(), is_exit=True)) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print(self.__salut), is_exit=True)) \
            .build()

    def __do_login_as_student(self):
        print('Logging as a Student')

        user_name, token = do_login()

        user = Student.create(user_name, token)

        self.__handler = Handler(user)

        self.__menu = Menu.Builder(Description(self.__app_name), auto_select=lambda: self.__print_lessons()) \
            .with_entry(Entry.create('1', 'Book a lesson', on_selected=lambda: self.__book_lesson())) \
            .with_entry(Entry.create('2', 'Cancel a booking', on_selected=lambda: self.__cancel_booking())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print(self.__salut), is_exit=True)) \
            .build()

    def __do_login_as_teacher(self):
        print('Logging as a Teacher')

        user_name, token = do_login()
        user = Teacher.create(user_name, token)

        self.__handler = Handler(user)

        self.__menu = Menu.Builder(Description(self.__app_name), auto_select=lambda: self.__print_lessons()) \
            .with_entry(Entry.create('1', 'Create a lesson', on_selected=lambda: self.__create_lesson())) \
            .with_entry(Entry.create('2', 'Modify a lesson', on_selected=lambda: self.__modify_lesson())) \
            .with_entry(Entry.create('3', 'Cancel a lesson', on_selected=lambda: self.__cancel_lesson())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print(self.__salut), is_exit=True)) \
            .build()

    def __do_login_as_admin(self):
        print('Logging as an Admin')

        user_name, token = do_login()
        user = Admin.create(user_name, token)

        self.__handler = Handler(user)

        self.__menu = Menu.Builder(Description(self.__app_name), auto_select=lambda: self.__print_lessons()) \
            .with_entry(Entry.create('1', 'Get admin page link', on_selected=lambda: self.__get_admin_page())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print(self.__salut), is_exit=True)) \
            .build()

    def __print_lessons(self) -> None:
        # TODO: do a better format
        lessons_json = self.__handler.fetch_lessons()
        print(lessons_json)

    def __create_lesson(self):
        self.__handler.create_lesson(__setup_lesson())

    def __modify_lesson(self):
        self.__handler.modify_lesson(__setup_lesson())

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
            # print_exc()


def main():
    App().run()


if __name__ == "__main__":
    main()
