# coding: utf-8

import unittest

from minobr.people import PeopleOccupation, Teacher
from minobr.tests.fake_objects import combine_faculty
from minobr.university.faculty import FacultyTypes, Faculty
from minobr.university.group import Group
from minobr.university.staff import StaffType


class FacultyTest(unittest.TestCase):

    def test_faculty_add_group(self):
        hum_fac = Faculty('languages', FacultyTypes.hum)
        tech_fac = Faculty('tech', FacultyTypes.tech)
        self.assertEqual(hum_fac.type, FacultyTypes.hum)
        self.assertEqual(tech_fac.type, FacultyTypes.tech)
        g1 = Group('1')
        hum_fac.add_group(g1)
        self.assertTrue(hum_fac.groups)

    def test_faculty_add_workers(self):
        hum_fac = Faculty('languages', FacultyTypes.hum)
        self.assertEqual(hum_fac.type, FacultyTypes.hum)
        p1 = Teacher(name='test_user')
        p1.add_employment(PeopleOccupation.employee, 'teacher')

        hum_fac.add_staff(StaffType.teachers, p1)
        self.assertTrue(hum_fac.staff()[StaffType.teachers])
