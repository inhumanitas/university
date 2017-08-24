# coding: utf-8

import unittest

from minobr.people import PeopleOccupation, Teacher
from minobr.university.staff import StaffUnit, StaffType


class StaffUnitTest(unittest.TestCase):
    Sam = None
    deanery = None

    def setUp(self):
        super(StaffUnitTest, self).setUp()

        self.deanery = StaffUnit(StaffType.management)
        self.Sam = Teacher(name='Sam')
        self.position = 'test_position'
        self.deanery.hire_person(self.Sam, self.position)

    def tearDown(self):
        super(StaffUnitTest, self).tearDown()
        self.Sam = None
        self.deanery = None

    def test_adding_unemployed(self):

        self.assertEqual(len(self.Sam.experiences), 1)
        self.assertIn(self.position,
                      [p.position for p in self.Sam.experiences])

    def test_hiring(self):

        self.assertIn(PeopleOccupation.employee, self.Sam.occupations)

        self.assertTrue(self.deanery.workers())

    def test_firing(self):
        self.assertIn(PeopleOccupation.employee, self.Sam.occupations)

        self.assertTrue(self.deanery.workers())

        self.deanery.fire_person(self.Sam, self.position)
