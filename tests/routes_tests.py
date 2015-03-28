#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-28 21:59:34
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import asyncio

from apostles.providers.route import Export as RouteProvider


class Handler(object):
    pass

handler = Handler()
RouteProvider().register(handler)


def test_init():
    assert handler.route_provider._application is handler


@asyncio.coroutine
def test_add_and_url():
    @asyncio.coroutine
    def test():
        pass
    handler.add_url_rule("GET", "/path", test)
    assert handler.route_provider.url(
        "test", query={"name": 1}) == "/path?name=1"


@asyncio.coroutine
def test_route_decorator():
    @handler.route("/path_a")
    @asyncio.coroutine
    def test_A():
        pass
    assert handler.route_provider.url(
        "test_a", query={"name": 1}) == "/path_a?name=1"
