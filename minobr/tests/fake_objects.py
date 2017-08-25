# coding: utf-8
import random
from functools import wraps

from faker import Faker

from minobr.people import PeopleOccupation
from minobr.university.faculty import Faculty
from minobr.university.group import Group, Student
from minobr.university.semestr import Semester
from minobr.university.topics import Topic
from minobr.university.staff import StaffType, Teacher

faker = Faker()


def _gen_teacher(**kwargs):
    while True:
        teacher = Teacher(name=faker.name(), last_name=faker.last_name(),
                          **kwargs)
        yield teacher


def _gen_student(faculty, group):

    while True:
        student = Student(faculty, group, name=faker.name())
        yield student


def create_teacher(**kwargs):
    return next(_gen_teacher(**kwargs))


TOPICS = [
    # knowledge area: lesson list
    {'math': ['matan', 'algebra']},
    {'lang': ['grammar', 'writing']},
]

for i in range(100):
    TOPICS.append({
        faker.word(): [Topic(w, create_teacher()) for w in faker.words()]
    })


def create_student(faculty, group):
    return next(_gen_student(faculty, group))


def one_or_many(f):
    @wraps(f)
    def inner(*args, **kwargs):
        result = f(*args, **kwargs)
        return result[0] if len(result) == 1 else result
    return inner


@one_or_many
def create_group(faculty, count=1, students_count=10):
    groups = []
    for i in range(count):
        group = Group(faker.word())
        for cur in range(students_count):
            s1 = Student(faculty, group, name=faker.name())
            group.add(s1)
        groups.append(group)
    return groups


@one_or_many
def combine_faculty(f_type, count=1, staff_count=10, student_count=30):
    f_list = []
    for i in range(count):
        f = Faculty(faker.name(), f_type)
        for p_count in range(staff_count):
            t1 = create_teacher()
            t2 = create_teacher()
            f.hire(StaffType.teachers, t1, faker.job())
            f.hire(StaffType.management, t2, faker.job())

        f.add_group(create_group(f, students_count=student_count))
        teachers = f.staff()[StaffType.teachers].list()
        teachers_count = len(teachers)
        for number in range(1, 4):
            s = Semester(1, number, f)
            for _ in range(random.randrange(10, len(TOPICS))):
                s.add_topic(Topic(faker.word(),
                                  teachers[random.randrange(0, teachers_count)]))
            f.add_semester(s)

        f_list.append(f)
    return f_list
