#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-28 18:56:54
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import asyncio
from aiohttp.web import UrlDispatcher

from .abc import Provider
from apostles.utils import SingletonDecorator, pythonify_name


@SingletonDecorator
class RouteProvider():

    def __init__(self, application):
        self._dispatcher = UrlDispatcher()
        self._application = application

    def add_url_rule(self, method, path, handler, *, name=None):
        name = name or pythonify_name(handler.__name__)
        print(name)
        self._dispatcher.add_route(method, path, handler, name=name)

    def add_with_decorator(self, path, *, method="GET", name=None):
        def _wrapper(fn):
            self.add_url_rule(method, path, fn, name=name)
            return fn
        return _wrapper

    @asyncio.coroutine
    def resolve(self, request):
        """
        根据请求里面的 method 和 path 找到对应的 match dict
        """
        return (yield from self._dispatcher.resolve(request))

    def url(self, name, **kwargs):
        assert name in self._dispatcher
        return self._dispatcher[name].url(**kwargs)


class Export(Provider):

    @staticmethod
    def register(application):
        route_provider = RouteProvider(application)
        setattr(application, "add_url_rule", route_provider.add_url_rule)
        setattr(application, "route_provider", route_provider)
        setattr(application, "route", route_provider.add_with_decorator)
