# coding: utf-8
from datetime import datetime

from collections import defaultdict

from minobr.people import PeopleOccupation, Unit, Person, OccupiedPersonMixin


class Schedule(object):
    topic = None
    date = None
    passed = False
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
        self.time_table = defaultdict(list)

    @staticmethod
    def _generate_key(*args):
        return '_'.join(map(unicode, args))

    def new_topic_entrance(self, date, topic):
        schedule = Schedule(topic)
        schedule.date = date
        self.time_table[self._generate_key(topic)].append(schedule)

    def set_attending(self, date, topic, attended, skipped):
        schedule_lst = self.time_table.get(self._generate_key(topic))
        if not schedule_lst:
            raise ValueError('Schedule entry not found')

        for schedule in schedule_lst:
            if not schedule.passed and schedule.date == date:
                schedule.passed = True
                break
        else:
            schedule = Schedule(topic)
            schedule.date = date
            schedule_lst.append(schedule)

        schedule.set_attending(date, attended, skipped)
        return schedule

    def get_timetable(self):
        return self.time_table

    def get_schedules(self, date, topic):
        assert isinstance(date, datetime)
        schedules = self.time_table.get(self._generate_key(topic))

        if not schedules:
            raise ValueError('Schedule entry not found')

        return schedules


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

    def get_timetable(self):
        return self._scheduler.get_timetable()

    def get_schedules(self, date, topic):
        return self._scheduler.get_schedules(date, topic)


class Student(Person, OccupiedPersonMixin):
    _faculty = None
    _group = None

    def __init__(self, faculty, group, **kwargs):
        super(Student, self).__init__(**kwargs)
        self._faculty = faculty
        self._group = group
