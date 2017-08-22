# coding: utf-8

from minobr.helpers import Composite
from minobr.university.faculty import Faculty


class University(Composite):
    item_class = Faculty

    staff_list = None

    def add_staff(self, person):
        self.staff_list.add(person)
