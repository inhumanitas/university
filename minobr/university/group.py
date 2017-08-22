# coding: utf-8

from minobr.people import PeopleOccupation, Unit


class Group(Unit):

    name = None

    def __init__(self, name):
        super(Group, self).__init__()
        self.name = name
        self._students = set()

    def validate(self, item):
        super(Group, self).validate(item)
        assert PeopleOccupation.student in item.occupations
