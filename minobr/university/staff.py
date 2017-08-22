# coding: utf-8

from collections import defaultdict

from minobr.helpers import Enum
from minobr.people import PeopleOccupation, Unit


class StaffType(object):
    __metaclass__ = Enum

    teachers = 'teachers'
    management = 'management'


class StaffUnit(Unit):

    def __init__(self, staff_type):
        super(StaffUnit, self).__init__()
        self.staff_type = staff_type
        self._workers = defaultdict(list)

    def hire_person(self, person, position):
        person.add_employment(PeopleOccupation.employee, position)
        self._workers[person].append(position)

    def fire_person(self, person, position):
        person.free_employment(PeopleOccupation.employee, position)
        self._workers[person].remove(position)

    def workers(self):
        return self._workers
