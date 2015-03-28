#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-28 19:04:32
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import re


def pythonify_name(name):
    name = re.sub('([a-z_])([A-Z][_a-z])', '\\1 \\2', name)
    return re.sub('[^\w+]', '_', name.lower())


class SingletonDecorator:

    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self, *args, **kwds):
        if self.instance == None:
            self.instance = self.klass(*args, **kwds)
        return self.instance
