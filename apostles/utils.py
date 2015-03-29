#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-28 19:04:32
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com


class SingletonDecorator:

    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self, *args, **kwds):
        if self.instance == None:
            self.instance = self.klass(*args, **kwds)
        return self.instance
