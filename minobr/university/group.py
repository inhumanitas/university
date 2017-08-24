# coding: utf-8
from datetime import datetime

from minobr.people import PeopleOccupation, Unit, Person, OccupiedPersonMixin


class Schedule(object):
    topic = None
    date = None
    student_attended = None
    student_skipped = None

    def __init__(self, topic):
        super(Schedule, self).__init__()
        self.topic = topic

    def set_attending(self, date, attended_student, skipped_students=None):
        self.date = date
        if skipped_students is None:
            skipped_students = []
        assert all([
            isinstance(s, Student) and PeopleOccupation.student in s.occupations
            for s in attended_student])
        assert all([
            isinstance(s, Student) and PeopleOccupation.student in s.occupations
            for s in skipped_students])

        self.student_attended = attended_student
        self.student_skipped = skipped_students

    def is_attended(self, student):
        assert isinstance(student, Student)
        if (student not in self.student_skipped and
                student in self.student_attended):
            return self.date


class _Scheduler(object):
    time_table = None

    def __init__(self):
        super(_Scheduler, self).__init__()
        self.time_table = {}

    @staticmethod
    def _generate_key(*args):
        return '_'.join(map(unicode, args))

    def new_topic_entrance(self, date, topic):
        self.time_table[self._generate_key(date, topic)] = Schedule(topic)

    def set_attending(self, date, topic, attended, skipped):
        schedule = self.time_table.get(self._generate_key(date, topic))
        if not schedule:
            raise ValueError('Schedule entry not found')
        schedule.set_attending(date, attended, skipped)
        return schedule

    def attended(self, date, topic):
        assert isinstance(date, datetime)
        schedule = self.time_table.get(self._generate_key(date, topic))
        if not schedule:
            raise ValueError('Schedule entry not found')

        return schedule.student_attended

    def skipped(self, date=None, topic=None):
        if date and topic:
            assert isinstance(date, datetime)
            schedule = self.time_table.get(self._generate_key(date, topic))
            if not schedule:
                raise ValueError('Schedule entry not found')
            schedules = [schedule]
        else:
            schedules = self.time_table.values()

        return sum([sch.student_skipped for sch in schedules],[])


class Group(Unit):

    name = None
    _scheduler = None

    def __init__(self, name):
        super(Group, self).__init__()
        self._scheduler = _Scheduler()
        self.name = name
        self._students = set()

    def validate(self, item):
        super(Group, self).validate(item)
        assert PeopleOccupation.student in item.occupations

    def dismiss(self, student):
        assert isinstance(student, Student)
        self.remove(student)

    def set_attending(self, date, topic, attended, skipped=None):
        return self._scheduler.set_attending(date, topic, attended, skipped)

    def new_topic_entrance(self, date, topic):
        return self._scheduler.new_topic_entrance(date, topic)

    def skipped(self, date=None, topic=None):
        return self._scheduler.skipped(date, topic)

    def attended(self, date, topic):
        return self._scheduler.attended(date, topic)


class Student(Person, OccupiedPersonMixin):
    _faculty = None
    _group = None

    def __init__(self, faculty, group, **kwargs):
        super(Student, self).__init__(**kwargs)
        self._faculty = faculty
        self._group = group
