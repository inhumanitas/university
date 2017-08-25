# coding: utf-8

from collections import defaultdict
from datetime import datetime

from minobr.helpers import Enum, Composite


class PeopleOccupation(object):
    """
    Types of people occupation
    """
    __metaclass__ = Enum

    student = 'student'
    employee = 'employee'
    unemployed = 'unemployed'
    values = {
        student: 'a student',
        employee: 'an employee',
        unemployed: 'unemployed',
    }


class Person(object):
    """
    Person from real world
    """
    name = None
    f_name = None
    l_name = None

    def __init__(self, **kwargs):
        super(Person, self).__init__()

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return u"<{type}> {name}".format(type=self.__class__.__name__,
                                         name=getattr(self, u'name', u''))


class PersonExperience(object):
    """
    People can work. Work is last an experience for occupied position.
    """
    position = None
    _start_date = None
    _quit_date = None

    def __init__(self, position, start_date=None):
        super(PersonExperience, self).__init__()
        assert position
        self.position = position
        self._start_date = start_date or datetime.now()

    def __repr__(self):
        fmt = '%d.%Y'
        return u"<{pos}> - [{start}..{end}]".format(
            pos=self.position,
            start=self._start_date.strftime(fmt),
            end=self._quit_date.strftime(fmt) if self._quit_date else '')

    @property
    def start_date(self):
        return self._start_date

    @property
    def quit_date(self):
        return self._quit_date

    def quit(self, quit_date=None):
        """
        Close working experience for people
        :param quit_date: The last working day for the occupied position
        """
        assert not self._quit_date, "Working in closed experience period"
        if quit_date is None:
            quit_date = datetime.now()
        if self._start_date >= quit_date:
            raise ValueError("Wrong quit date")

        self._quit_date = quit_date


class OccupiedPersonMixin(object):

    _occupations = None  # current persons occupations
    _experiences = None  # persons work\study experiences

    def __init__(self):
        super(OccupiedPersonMixin, self).__init__()
        self._experiences = defaultdict(list)
        self.unemployed()

    def __repr__(self):
        base = super(OccupiedPersonMixin, self).__repr__()
        return base + u" is %s" % (
            (unicode(
                u" and ".join(
                    [PeopleOccupation.values[o] for o in self.occupations]) or
                u"unemployed"))
        )

    @property
    def experiences(self):
        return sum(self._experiences.values(), [])

    @property
    def occupations(self):
        return self._occupations

    def add_employment(self, occupation_type, position):
        assert occupation_type in PeopleOccupation
        if PeopleOccupation.unemployed in self._occupations:
            self._occupations.remove(PeopleOccupation.unemployed)
        self._occupations.add(occupation_type)
        self._experiences[occupation_type].append(PersonExperience(position))
        self._check_employment()
        return self.occupations

    def _check_employment(self):
        if PeopleOccupation.unemployed in self.occupations:
            assert len(self.occupations) == 1

    def unemployed(self):
        for exp_type in self._experiences:
            for exp in self._experiences[exp_type]:
                exp.quit()
        self._occupations = {PeopleOccupation.unemployed}

    def free_employment(self, occupation_type, position):
        if occupation_type == PeopleOccupation.unemployed:
            for exp_type in self._experiences:
                for exp in self._experiences[exp_type]:
                    if position == exp.position:
                        exp.quit()
            self._occupations = {PeopleOccupation.unemployed}
        else:
            self._occupations.remove(occupation_type)
            if occupation_type in self._experiences:
                for exp in self._experiences[occupation_type]:
                    exp.quit()
        self._check_employment()


class Unit(Composite):
    item_class = Person
