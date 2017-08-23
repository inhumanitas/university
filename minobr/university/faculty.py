# coding: utf-8

from minobr.helpers import Enum
from minobr.people import PeopleOccupation
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
        return self._groups

    def add_group(self, group):
        self._groups.add(group)

    def add_semester(self, semester):
        self._semester.add(semester)

    def add_staff(self, staff_type, people, position):
        assert staff_type in self.staff()
        assert PeopleOccupation.employee in people.occupations
        self.staff()[staff_type].add(people)

    def staff(self):
        return {
            StaffType.management: self._managements,
            StaffType.teachers: self._teachers,
        }
