import unittest.mock


def jitclass(spec):
    def wrapper(func):
        def wrapper2(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper2
    return wrapper

typeof = lambda a: None
types = unittest.mock.Mock()
