#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-28 23:46:34
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import asyncio
import unittest
from inspect import getsourcefile
from os import path

from functools import wraps

CURRENT_PATH = path.join(
    path.dirname(path.abspath(getsourcefile(lambda _: None))), "example")


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()

    def tearDown(self):
        self.loop.close()
        del self.loop


def run_until_complete(fun):
    if not asyncio.iscoroutinefunction(fun):
        fun = asyncio.coroutine(fun)

    @wraps(fun)
    def wrapper(test, *args, **kw):
        loop = test.loop
        ret = loop.run_until_complete(fun(test, *args, **kw))
        return ret
    return wrapper
