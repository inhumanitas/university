# coding: utf-8


class Enum(type):

    def __contains__(self, item):
        return item in self.__dict__.values()


class Composite(object):
    item_class = None
    _items = None

    def __init__(self):
        super(Composite, self).__init__()
        self._items = set()
        assert self.item_class

    def validate(self, item):
        assert issubclass(item.__class__, self.item_class)

    def add(self, item):
        self.validate(item)
        self._items.add(item)

    def remove(self, item):
        self.validate(item)
        self._items.remove(item)

    def list(self):
        return self._items
