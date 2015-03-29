#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-28 21:59:34
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import asyncio

from apostles.providers.route import Export as RouteProvider
from .utils import run_until_complete, BaseTest
from apostles.web import Application


class Handler(object):
    pass
handler = Handler()


class RouteTests(BaseTest):

    @asyncio.coroutine
    def init(self):
        self.handler = handler
        return (yield from RouteProvider().register(self.handler))

    @run_until_complete
    def test_init(self):
        yield from self.init()
        self.assertTrue(
            self.handler.route_provider._application is self.handler)

    @run_until_complete
    def test_add_and_url(self):
        yield from self.init()

        @asyncio.coroutine
        def test():
            pass
        self.handler.add_url_rule("GET", "/path", test)
        self.assertTrue(self.handler.route_provider.url(
            "test", query={"name": 1}) == "/path?name=1")

    @run_until_complete
    def test_route_decorator(self):
        yield from self.init()

        @self.handler.route("/path_a")
        @asyncio.coroutine
        def test_A():
            pass
        self.assertTrue(self.handler.route_provider.url(
            "test_a", query={"name": 1}) == "/path_a?name=1")

    @run_until_complete
    def test_resolve(self):
        yield from self.init()

        @self.handler.route("/path_a/{id}")
        @asyncio.coroutine
        def test_C():
            pass

        class TestReq(object):
            method = "GET"
            path = "/path_a/12"

        r = yield from self.handler.route_provider.resolve(TestReq())
        self.assertTrue(r["id"] == "12")
        self.assertTrue(r._route.name == "test_c")

    @run_until_complete
    def test_with_application(self):
        app = Application()
        yield from app._register_provider()
        self.assertTrue(app.route_provider.url(
            "test_a", query={"name": 1}) == "/path_a?name=1")
