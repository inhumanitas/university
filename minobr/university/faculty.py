# coding: utf-8
from collections import defaultdict

from minobr.helpers import Enum
from minobr.people import PeopleOccupation
from minobr.university.management import Management, NotAllowedException
from minobr.university.staff import StaffType, StaffUnit


class FacultyTypes(object):
    __metaclass__ = Enum

    tech = 'technical'
    hum = 'humanitarian'


class Faculty(object):

    _f_type = None

    name = None

    def __init__(self, name, f_type):
        super(Faculty, self).__init__()
        assert f_type in FacultyTypes
        self._f_type = f_type
        self.name = name
        self._managements = StaffUnit(StaffType.management)
        self._teachers = StaffUnit(StaffType.teachers)
        self._groups = set()
        self._semesters = set()

    def __repr__(self):
        return u"<Faculty %s> %s" % (self.type, self.name)

    @property
    def type(self):
        return self._f_type

    @property
    def groups(self):
        return list(self._groups)

    @property
    def semesters(self):
        return list(self._semesters)

    def add_group(self, group):
        self._groups.add(group)

    def add_semester(self, semester):
        self._semesters.add(semester)

    def hire(self, staff_type, person, position):
        assert staff_type in self.staff()
        self.staff()[staff_type].hire_person(person, position)

    def staff(self):
        return {
            StaffType.management: self._managements,
            StaffType.teachers: self._teachers,
        }

    def is_working(self, person):
        return any(map(lambda staff_unit: person in staff_unit.list(),
                   self.staff().values()))

    def is_manager(self, person):
        return any(map(lambda manager: person == manager,
                       self.staff()[StaffType.management].list()))


def allowed(fn):
    def is_working_manager(self):
        return (self.management_obj.is_working(self.manager) and
                self.management_obj.is_manager(self.manager))

    checkers = {
        'hire': is_working_manager,
        'dismiss_student': is_working_manager,
        'change_topic_teacher': is_working_manager,
    }

    def inner(self, *args, **kwargs):
        checker = checkers.get(fn.__name__)
        if checker and checker(self):
            return fn(self, *args, **kwargs)
        raise NotAllowedException()
    return inner


class FacultyManagement(Management):

    def __init__(self, management_obj):
        self.management_obj = management_obj

    @allowed
    def change_topic_teacher(self, topic, new_teacher):
        if topic.teacher.knowledge_area == new_teacher.knowledge_area:
            topic.teacher = new_teacher

    @allowed
    def hire(self, staff_type, people, position):
        return self.management_obj.hire(staff_type, people, position)

    @allowed
    def dismiss_student(self, student):
        assert PeopleOccupation.student in student.occupations
        st_group = None
        for group in self.management_obj.groups:
            if student in group.list():
                st_group = group
                break
        if not st_group:
            raise ValueError('Student not enrolled')

        st_group.dismiss(student)

    def staff(self):
        return self.management_obj.staff()

    def students_to_fire(self, group=None):

        topic_enrollment = {}
        topic_lesson_count = {}
        fire_students = defaultdict(int)
        for cur_group in self.management_obj.groups:
            if group is not None and cur_group != group:
                continue

            students_enrolment = defaultdict(int)
            for topic, schedules in cur_group.get_timetable().items():
                for schedule in schedules:
                    for skipped_student in schedule.student_skipped:
                        students_enrolment[skipped_student] += 1
                topic_enrollment[topic] = students_enrolment
                topic_lesson_count[topic] = len(schedules)

                min_enroll = len(schedules) * 60 / 100
                for _topic, student_enroll_dict in topic_enrollment.items():
                    for student, value in student_enroll_dict.items():
                        if ((value > min_enroll) and
                                (topic_lesson_count[_topic] > value)):
                            student_enroll_dict.pop(student)

            for topic, students in topic_enrollment.items():
                for student in students:
                    fire_students[student] += 1

            fire_students = filter(lambda x: x >= 3, fire_students)

        return fire_students
