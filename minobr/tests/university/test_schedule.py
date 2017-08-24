# coding: utf-8

import unittest

from datetime import datetime

from minobr.tests.fake_objects import combine_faculty
from minobr.university.faculty import FacultyTypes
from minobr.university.staff import StaffType
from minobr.university.topics import Topic


class ScheduleTest(unittest.TestCase):
    def setUp(self):
        super(ScheduleTest, self).setUp()
        self.faculty = combine_faculty(FacultyTypes.hum)

    def test_attending(self):
        teachers = self.faculty.staff()[StaffType.teachers].list()
        topic = Topic('sda', teachers[0])
        attend_date = datetime.now()
        self.assertTrue(teachers)

        groups = self.faculty.groups
        self.assertTrue(groups)

        group = groups[0]
        students = group.list()
        teacher = teachers[0]
        st_count = len(students)
        attended = students[:st_count]
        skipped = students[st_count:]
        teacher.schedule_topic(group, attend_date, topic)
        teacher.set_attending(group, attend_date, topic, attended, skipped)

        schedules = group.get_schedules(attend_date, topic)
        for schedule in schedules:
            self.assertEqual(skipped, schedule.student_skipped)
            self.assertEqual(attended, schedule.student_attended)

    def test_no_entry_schedule(self):
        teachers = self.faculty.staff()[StaffType.teachers].list()
        topic = Topic('sda', teachers[0])
        attend_date = datetime.now()
        self.assertTrue(teachers)

        groups = self.faculty.groups
        self.assertTrue(groups)

        group = groups[0]
        students = group.list()
        teacher = teachers[0]
        st_count = len(students)
        attended = students[:st_count]
        skipped = students[st_count:]
        self.assertRaises(ValueError, teacher.set_attending,
                          group, attend_date, topic, attended, skipped)
