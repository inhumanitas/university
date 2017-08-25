# coding: utf-8
import unittest

from minobr.people import PeopleOccupation
from minobr.tests.fake_objects import combine_faculty
from minobr.university.faculty import FacultyTypes
from minobr.university.group import Group, Student


class GroupTest(unittest.TestCase):

    def test_group_add(self):
        f = combine_faculty(FacultyTypes.hum)
        student = Student(f, f.groups[0])
        group1 = Group('1')

        group1.add(student)
        self.assertTrue(group1.list())
        self.assertIn(student, group1.list())
