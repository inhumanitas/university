# coding: utf-8
import unittest

from faker import Faker

from minobr.people import PeopleOccupation
from minobr.tests.fake_objects import create_teacher, combine_faculty
from minobr.university.faculty import FacultyManagement, FacultyTypes
from minobr.university.group import Student
from minobr.university.management import NotAllowedException
from minobr.university.staff import StaffType

faker = Faker()


class RolesTest(unittest.TestCase):
    def test_not_allowed_perms(self):
        teacher = create_teacher()
        f_mng = FacultyManagement(combine_faculty(FacultyTypes.tech))
        f_mng.set_manager(teacher)

        self.assertRaises(NotAllowedException, f_mng.hire,
                          StaffType.teachers, create_teacher(), 'teacher')

    def test_allowed_perms(self):
        f_mng = FacultyManagement(combine_faculty(FacultyTypes.tech))

        manager = f_mng.management_obj.staff()[StaffType.management].list()[0]
        f_mng.set_manager(manager)

        teacher = create_teacher()
        f_mng.hire(StaffType.teachers, teacher, 'teacher')

        self.assertIn(teacher, f_mng.staff()[StaffType.teachers].list())

    def test_dismiss_student(self):
        faculty = combine_faculty(FacultyTypes.tech)
        f_mng = FacultyManagement(faculty)
        manager = f_mng.management_obj.staff()[StaffType.management].list()[0]
        f_mng.set_manager(manager)

        student = Student(faculty, faculty.groups[0])
        student.add_employment(PeopleOccupation.student, 'student')
        self.assertRaises(ValueError, f_mng.dismiss_student, student)

        group = faculty.groups[0]
        student = group.list()[0]

        self.assertIn(student, group.list())

        f_mng.dismiss_student(student)

        self.assertNotIn(student, group.list())

    def test_dismiss_skipped_students(self):
        faculty = combine_faculty(FacultyTypes.tech)
        f_mng = FacultyManagement(faculty)
        manager = f_mng.management_obj.staff()[StaffType.management].list()[0]
        f_mng.set_manager(manager)
        group = faculty.groups[0]

        student = group.list()[0]
        student1 = group.list()[1]

        semester = faculty.semesters[0]

        topics = list(semester.topics)[:len(semester.topics)/3]
        semester.enroll(student, topics)
        semester.enroll(student1, topics)

        enroll_count = 20
        pass_count = enroll_count * 60 / 100
        for topic in topics:
            teacher = topic.teacher
            for count in range(enroll_count):
                date = faker.date()
                teacher.schedule_topic(group, date, topic)
                if count < pass_count:
                    group.set_attending(date, topic, [student], [student1])
                else:
                    group.set_attending(date, topic, [student, student1])

        to_fire_students = f_mng.students_to_fire(group)

        self.assertNotIn(student, to_fire_students)
        self.assertIn(student1, to_fire_students)
