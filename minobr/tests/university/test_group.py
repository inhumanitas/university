# coding: utf-8
import unittest

from minobr.people import Person, PeopleOccupation
from minobr.university.group import Group


class GroupTest(unittest.TestCase):

    def test_group_add(self):
        John = Person()
        group1 = Group('1')
        self.assertRaises(AssertionError, group1.add, John)

        John.add_employment(PeopleOccupation.student, group1.name)
        group1.add(John)
        self.assertTrue(group1.list())
