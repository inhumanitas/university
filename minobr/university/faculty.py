# coding: utf-8

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
        self._semester = set()

    @property
    def type(self):
        return self._f_type

    @property
    def groups(self):
        return list(self._groups)

    def add_group(self, group):
        self._groups.add(group)

    def add_semester(self, semester):
        self._semester.add(semester)

    def add_staff(self, staff_type, people):
        assert staff_type in self.staff()
        assert PeopleOccupation.employee in people.occupations
        self.staff()[staff_type].add(people)

    def staff(self):
        return {
            StaffType.management: self._managements,
            StaffType.teachers: self._teachers,
        }

    def is_working(self, person):
        return any(map(lambda staff_unit: person in staff_unit.list(),
                   self.staff().values()))


def allowed(fn):
    def add_staff_check(self):
        return (self.management_obj.is_working(self.manager) and
                self.management_obj.is_manager(self.manager))

    checkers = {
        'add_staff': add_staff_check
    }

    def inner(self, *args, **kwargs):
        checker = checkers.get(fn.__name__)
        if checker and checker(self):
            return fn(*args, **kwargs)
        raise NotAllowedException()
    return inner


class FacultyManagement(Management):

    def __init__(self, management_obj):
        self.management_obj = management_obj

    @allowed
    def add_staff(self, staff_type, people, position):
        self.management_obj.add_staff(staff_type, people, position)

    def dismiss_student(self, student):
        assert PeopleOccupation.student in student.occupations
        self.management_obj.groups