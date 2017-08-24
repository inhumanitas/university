# coding: utf-8
from unittest import TestCase

from minobr.tests.fake_objects import (
    combine_faculty, TOPICS, create_teacher, create_student)
from minobr.university.faculty import FacultyTypes
from minobr.university.semestr import Semester, SemesterException
from minobr.university.topics import Topic


class SemesterTests(TestCase):

    def test_enrollments_non_existing(self):
        faculty = combine_faculty(FacultyTypes.hum)
        s = Semester(1, 1, faculty)
        for topics in TOPICS:
            for topic in topics.values():
                s.add_topic(Topic(topic, create_teacher()))

        non_existing_topic = ''
        self.assertRaises(SemesterException,
                          s.enroll,
                          create_student(faculty, faculty.groups[0]),
                          [non_existing_topic])

    def test_hum_fac_enrollments(self):
        faculty = combine_faculty(FacultyTypes.hum)
        s = Semester(1, 1, faculty)
        for topics in TOPICS:
            for topic in topics.values():
                s.add_topic(Topic(topic, create_teacher()))

        self.assertTrue(s.enroll(create_student(faculty, faculty.groups[0]),
                        list(s.topics)[:len(s.topics)/2]))

    def test_tech_fac_enrollments(self):
        faculty = combine_faculty(FacultyTypes.tech)
        s = Semester(1, 1, faculty)
        for topics in TOPICS:
            for topic in topics.values():
                s.add_topic(Topic(topic, create_teacher()))

        self.assertTrue(s.enroll(create_student(faculty, faculty.groups[0]),
                        list(s.topics)[:len(s.topics)/2]))

    def test_multiple_enrollments(self):
        faculty = combine_faculty(FacultyTypes.tech)
        s = Semester(1, 1, faculty)
        for topics in TOPICS:
            for topic in topics.values():
                s.add_topic(Topic(topic, create_teacher()))

        enrolments = 10
        for current in range(enrolments):
            s.enroll(create_student(faculty, faculty.groups[0]),
                     list(s.topics)[:len(s.topics) / 2])

        self.assertEqual(len(s.enrollments), enrolments)
