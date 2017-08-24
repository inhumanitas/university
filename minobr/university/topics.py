# coding: utf-8

TOPICS = []


class Topic(object):
    name = None
    teacher = None

    def __init__(self, name, teacher):
        super(Topic, self).__init__()
        assert all((name, teacher))
        self.name = name
        self.teacher = teacher

    def __repr__(self):
        return u"<Topic> %s by %s" % (self.name, self.teacher)
