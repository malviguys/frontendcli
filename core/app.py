import datetime
import requests
import subprocess

from domain_objects.cost import Cost
from domain_objects.lesson import Lesson, Instrument
from domain_objects.user import Admin, Student, Teacher, User, Username
from menu.handler import Handler, API_SERVER_ADDRESS
from menu.menu import Description, Entry, Menu

from getpass import getpass

ADMIN_PAGE = ''


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

    def __setup_lesson(self):
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
        cost = input("Insert the cost of the lesson: ~ format: {00.00} ~")
        print(f'{name}, {instrument}, {teacher}, {date_time}, {duration}, {cost}')

        if any(x for x in Instrument if x.name == instrument.upper()):
            lesson = Lesson.create(name, teacher, Instrument[instrument.upper()], date_time=date_time,
                                   duration=duration, cost=Cost.parse(cost))
            return lesson
        else:
            print("Sorry, the given instrument was not correct!\n")
            return None


    def __do_login(self):
        while True:
            user_name = input('Insert your username:')
            pwd = getpass('Insert your password:')

            payload = dict(username=user_name, password=pwd)

            response = requests.post(f'{API_SERVER_ADDRESS}/auth/login/', data=payload)
            print(response.status_code)
            print(requests.codes.ok)
            if response.status_code != requests.codes.ok:
                print("Invalid credential, please try again.\n")
                continue

            token = response.json()['key']
            print('Successfully logged in!\n')
            return user_name, token

    def __do_login_as_student(self):
        print('Logging as a Student')

        user_name, token = self.__do_login()

        user = Student.create(user_name, token)

        self.__handler = Handler(user)

        self.__menu = Menu.Builder(Description(self.__app_name), auto_select=lambda: self.__print_lessons()) \
            .with_entry(Entry.create('1', 'Book a lesson', on_selected=lambda: self.__book_lesson())) \
            .with_entry(Entry.create('2', 'Cancel a booking', on_selected=lambda: self.__cancel_booking())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print(self.__salut), is_exit=True)) \
            .build()

    def __do_login_as_teacher(self):
        print('Logging as a Teacher')

        user_name, token = self.__do_login()
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

        user_name, token = self.__do_login()
        user = Admin.create(user_name, token)

        self.__handler = Handler(user)

        self.__menu = Menu.Builder(Description(self.__app_name), auto_select=lambda: self.__print_lessons()) \
            .with_entry(Entry.create('1', 'Get admin page link', on_selected=lambda: self.__get_admin_page())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print(self.__salut), is_exit=True)) \
            .build()

    def __print_lessons(self) -> None:
        lessons_json = self.__handler.fetch_lessons()
        print(lessons_json)

    def __create_lesson(self):
        lesson = self.__setup_lesson()
        if lesson is not None:
            if self.__handler.create_lesson(lesson):
                print(
                    f'Lesson "{lesson.lesson_name}" with {lesson.teacher} for {lesson.instrument.name} on {lesson.date_time} for '
                    f'{lesson.duration.seconds / 60 / 60} hours and {lesson.cost}€ created successfully!\n')
                # return lesson
            else:
                print('The lesson could not be created!\n')

    def __modify_lesson(self):
        lesson = self.__setup_lesson()
        if lesson is not None:
            if self.__handler.modify_lesson(lesson):
                print(
                    f'Lesson "{lesson.lesson_name}" with {lesson.teacher} for {lesson.instrument.name} successfully modified!\n')
            else:
                print('The lesson could not be modified!\n')

    def __cancel_lesson(self):
        lesson_id = input("Insert the id of the lesson to delete:")
        if self.__handler.cancel_lesson(lesson_id):
            print(f'Lesson "{lesson_id}" successfully cancelled!\n')
        else:
            print('Could not cancel lesson!\n')

    def __book_lesson(self) -> None:
        lesson_name = input("Insert the name of the lesson to book for:")
        if self.__handler.book_lesson(lesson_name):
            print(f'Successfully booked for lesson "{lesson_name}"!\n')
        else:
            print("Could not make booking for this lesson!\n")

    def __cancel_booking(self):
        lesson_name = input("Insert the name of the lesson to delete the reservation:")
        if self.__handler.cancel_booking(lesson_name):
            print(f'Successfully cancelled booking for "{lesson_name}"!\n')
        else:
            print("Could not cancel your booking!\n")

    def __get_admin_page(self):
        print(f'Admin page: {ADMIN_PAGE}')

    def __run(self) -> None:
        self.__login_menu.run()
        self.__menu.run()

    def run(self) -> None:
        # Updating the requirements
        subprocess.run(["pip", "install", "-r", ".\\requirements.txt"])
        try:
            self.__run()
        except Exception as e:
            print(e)
            print('Something went horribly wrong.')


def main():
    App().run()


if __name__ == "__main__":
    main()
