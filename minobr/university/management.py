# coding: utf-8


class NotAllowedException(Exception):
    pass


class Management(object):
    management_obj = None
    manager = None

    def set_manager(self, manager):
        self.manager = manager
