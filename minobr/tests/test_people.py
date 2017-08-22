# coding: utf-8
import unittest

from minobr.people import Person, employee_person, PeopleOccupation


class PeopleTest(unittest.TestCase):
    def test_name(self):
        Cain = Person(name='Cain')
        Adam = Person(name='Adam')

        self.assertNotEqual(Cain.name, Adam.name)

    def test_experience(self):
        Cain = Person(name='Cain')
        self.assertFalse(Cain.experiences)

    def test_employment(self):
        Adam = Person(name='Adam')
        Cain = Person(name='Cain')
        # Cain is a student
        employee_person(Cain, PeopleOccupation.student, 'First grade')
        # also he is working
        employee_person(Cain, PeopleOccupation.employee, 'Freelancer')
        self.assertTrue(Cain.experiences)

        employee_person(Adam, PeopleOccupation.employee, 'Translator')
        self.assertTrue(Adam.experiences)

        # left work and university
        Cain.unemployed()
        self.assertEqual(Cain.occupations, {PeopleOccupation.unemployed})
        for exp in Cain.experiences:
            self.assertTrue(exp.quit_date)
