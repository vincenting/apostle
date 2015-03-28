#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-28 16:56:17
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import asyncio


class Application(object):

    def __init__(self, root_name):
        self.sev = None

    def run(self, port=3000):
        loop = asyncio.get_event_loop()
        print('serving on', self.sev.sockets[0].getsockname())
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
