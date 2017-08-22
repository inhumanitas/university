# coding: utf-8
import unittest


def run_all_test():
    suite = unittest.TestLoader().discover(start_dir='.', pattern='test_*.py')
    runner = unittest.TextTestRunner().run(suite)
    return runner.wasSuccessful()


if __name__ == '__main__':
    run_all_test()
