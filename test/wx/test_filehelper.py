#!/usr/bin/env python
# encoding: utf-8
# @Time    : 10/18/18

__author__ = 'MiracleYoung'

import functools


def wraps(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)

        for item in args:
            print(item.__name__)
        return ret

    return _wrapper


class A:
    def __init__(self):
        self.meta = {
            'a': {
                'aa': 1
            }
        }

    @wraps
    def go(self, v):
        self.meta['b'] = v

import inspect
def get_current_function_name():
    return inspect.stack()[1][3]
class MyClass:
    def function_one(self):
        print("%s.%s invoked"%(self.__class__.__name__, get_current_function_name()))
if __name__ == "__main__":
    myclass = MyClass()
    myclass.function_one()