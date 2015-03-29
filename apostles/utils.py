#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-28 19:04:32
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import importlib


__import_cache = {}


def dynamic_import(parents, package, name):
    _id = str(parents) + package + name
    if _id in __import_cache:
        return __import_cache[_id]
    if len(parents) is 1:
        return importlib.import_module(".".join(
            [x for x in (parents[0], package, name) if x]
        ))
    for parent in parents:
        try:
            __import_cache[_id] = dynamic_import((parent, ), package, name)
            return __import_cache[_id]
        except ImportError:
            continue
    raise ImportError("Can not find {name} in {package}".format_map(
        {"package": package, "name": name}
    ))


class SingletonDecorator:

    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self, *args, **kwds):
        if self.instance == None:
            self.instance = self.klass(*args, **kwds)
        return self.instance
