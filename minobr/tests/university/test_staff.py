# coding: utf-8

import unittest

from minobr.people import PeopleOccupation
from minobr.tests.fake_objects import create_teacher, TOPICS, combine_faculty
from minobr.university.faculty import FacultyTypes, FacultyManagement
from minobr.university.staff import StaffUnit, StaffType, Teacher
from minobr.university.topics import Topic


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


class ManagerTest(unittest.TestCase):

    def test_change_topic_teacher(self):
        faculty = combine_faculty(FacultyTypes.tech)
        f_mng = FacultyManagement(faculty)
        manager = f_mng.management_obj.staff()[StaffType.management].list()[0]
        f_mng.set_manager(manager)

        topic_dict = TOPICS[0]
        kn_area = topic_dict.keys()[0]
        teacher1 = create_teacher(knowledge_area=kn_area)
        teacher2 = create_teacher(knowledge_area=kn_area)

        topic = Topic(topic_dict[kn_area][0], teacher1)

        f_mng.change_topic_teacher(topic, teacher2)
        self.assertEqual(topic.teacher, teacher2)
