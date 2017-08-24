# coding: utf-8
from minobr.people import Person, PeopleOccupation
from minobr.university.faculty import FacultyTypes


class SemesterException(Exception):
    pass


class Enroll(object):
    percent = None

    @classmethod
    def check_topics(cls, semester, student_topics):
        raise NotImplemented()


class TechFacultyEnroll(Enroll):
    percent = 80

    @classmethod
    def check_topics(cls, semester, student_topics):
        min_topic_count = len(semester.topics) * cls.percent / 100

        if min_topic_count < len(student_topics):
            raise SemesterException(
                "Min topic count is %s" % min_topic_count)


class HumFacultyEnroll(Enroll):
    percent = 70

    @classmethod
    def check_topics(cls, semester, student_topics):
        min_topic_count = len(semester.topics) * cls.percent / 100

        if min_topic_count < len(student_topics):
            raise SemesterException(
                "Min topic count is %s" % min_topic_count)


class Enrollment(object):
    enroll = None
    enrollments = {
        FacultyTypes.hum: HumFacultyEnroll,
        FacultyTypes.tech: TechFacultyEnroll
    }

    def __init__(self, semester, student):
        super(Enrollment, self).__init__()
        self.semester = semester
        self.student = student

    def set_enrollment(self, enroll):
        self.enroll = enroll

    def check_topics(self, semester, student_topics):
        return self.enroll.check_topics(semester, student_topics)


class Semester(object):
    course = None
    number = None
    _enrolled = None
    _topics = None
    faculty = None

    def __init__(self, course, number, faculty):
        self._topics = set()
        self._enrolled = set()
        self.course = course
        self.number = number
        self.faculty = faculty

    @property
    def topics(self):
        return self._topics

    @property
    def enrollments(self):
        return self._enrolled

    def add_topic(self, topic):
        self._topics.add(topic)

    def enroll(self, student, topics):
        """
        Student desire to pick topics from semester topics
        :param student: student who requests topics to pick
        :param topics: list of selected topics, from semester topics
        :raises: SemesterException if some of topics could be picked by student
        :return: enroll instance
        """
        assert isinstance(student, Person)
        assert isinstance(topics, (list, set, tuple))
        assert PeopleOccupation.student in student.occupations

        if not self.topics.issuperset(topics):
            raise SemesterException("You must select topics from semester")

        enrollment = Enrollment(self, student)
        enrollment.set_enrollment(Enrollment.enrollments[self.faculty.type])
        enrollment.check_topics(self, topics)

        self._enrolled.add(enrollment)
        return enrollment
