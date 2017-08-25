# coding: utf-8
import unittest

from minobr.tests.fake_objects import create_teacher
from minobr.university.faculty import Faculty, FacultyTypes
from minobr.university.group import Group, Student
from minobr.university.staff import StaffType
from minobr.university.university import University


class UniversityTest(unittest.TestCase):
    def test_university_creation(self):
        u1 = University()
        f1 = Faculty('f1', FacultyTypes.tech)
        f2 = Faculty('f2', FacultyTypes.hum)
        g1 = Group('g1')
        g2 = Group('g2')
        g3 = Group('g3')
        people = []
        people_count = 100
        f1.add_group(g1)
        f2.add_group(g2)
        f2.add_group(g3)
        u1.add(f1)
        u1.add(f2)
        for i in range(people_count):
            if i < 50:
                g = g1
            elif 50 < i < 80:
                g = g2
            else:
                g = g3
            p = Student(f1, g, name='test_'+unicode(i))
            g.add(p)
            people.append(p)
        dean = create_teacher()
        f1.hire(StaffType.management, dean, 'dean')
        self.assertTrue(u1.list())
        self.assertTrue(u1.staff())
        for f in u1.list():
            self.assertTrue(f.groups)
            for g in f.groups:
                self.assertTrue(g.list())
