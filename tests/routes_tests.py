#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-28 21:59:34
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import asyncio

from apostles.providers.route import Export as RouteProvider


class Handler(object):
    pass


class RouteTests(object):

    @asyncio.coroutine
    def setUp(self):
        self.handler = Handler()
        yield from RouteProvider().register(self.handler)

    def test_init(self):
        assert self.handler.route_provider._application is self.handler

    @asyncio.coroutine
    def test_add_and_url(self):
        @asyncio.coroutine
        def test():
            pass
        self.handler.add_url_rule("GET", "/path", test)
        assert self.handler.route_provider.url(
            "test", query={"name": 1}) == "/path?name=1"

    @asyncio.coroutine
    def test_route_decorator(self):
        @self.handler.route("/path_a")
        @asyncio.coroutine
        def test_A():
            pass
        assert self.handler.route_provider.url(
            "test_a", query={"name": 1}) == "/path_a?name=1"
