# coding: utf-8
import unittest

from minobr.people import Person, PeopleOccupation
from minobr.university.faculty import Faculty, FacultyTypes
from minobr.university.group import Group
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
        for i in range(1000):
            p = Person(name='test_'+unicode(i))
            p.add_employment(PeopleOccupation.student, '1st grade')
            people.append(p)
            if i < 50:
                g1.add(p)
            elif i < 100:
                g2.add(p)
            else:
                g3.add(p)
        f1.add_group(g1)
        f2.add_group(g2)
        f2.add_group(g3)
        u1.add(f1)
        u1.add(f2)
