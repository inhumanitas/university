# coding: utf-8

from minobr.helpers import Composite
from minobr.university.faculty import Faculty


class University(Composite):
    item_class = Faculty

    staff_list = None

    def add_staff(self, person):
        self.staff_list.add(person)

    def staff(self, faculty=None):
        faculties = self.list()
        if faculty and faculty in faculties:
            faculties = [faculty]
        staff = set()
        for faculty in faculties:
            for staff_unit in faculty.staff().values():
                staff.update(staff_unit.list())
        return staff
