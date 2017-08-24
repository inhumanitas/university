# coding: utf-8
import unittest

from minobr.people import Person, PeopleOccupation
from minobr.university.group import Student
from minobr.tests.fake_objects import combine_faculty
from minobr.university.faculty import FacultyTypes


class PeopleTest(unittest.TestCase):
    def test_name(self):
        Cain = Person(name='Cain')
        Adam = Person(name='Adam')

        self.assertNotEqual(Cain.name, Adam.name)

    def test_employment(self):
        f1 = combine_faculty(FacultyTypes.hum)
        Adam = Student(f1, f1.groups[0], name='Adam')
        Cain = Student(f1, f1.groups[0], name='Cain')
        # Cain is a student
        Adam.add_employment(PeopleOccupation.student, 'First grade')
        # also he is working
        Cain.add_employment(PeopleOccupation.employee, 'Freelancer')
        self.assertTrue(Cain.experiences)

        Adam.add_employment(PeopleOccupation.employee, 'Translator')
        self.assertTrue(Adam.experiences)

        # left work and university
        Cain.unemployed()
        self.assertEqual(Cain.occupations, {PeopleOccupation.unemployed})
        for exp in Cain.experiences:
            self.assertTrue(exp.quit_date)
