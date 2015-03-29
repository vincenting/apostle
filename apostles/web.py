#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-28 16:56:17
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import asyncio
import inspect
import toml
import os
from pathlib import Path
from copy import deepcopy
from aiohttp.server import ServerHttpProtocol
from aiohttp import Response

from .utils import SingletonDecorator, dynamic_import
from .providers.abc import Provider


@SingletonDecorator
class Settings(object):

    def __init__(self, **kwarg):
        self._settings = kwarg
        self._settings["root_path"] = self._settings.get(
            "root_path", os.getcwd())
        self._config_file_cache = {}
        self._load_configs_from_config()
        self._settings["env"] = self._settings.get("env", None) or \
            os.environ.get("PYTHON_ENV", "development")

    def _load_configs_from_config(self):
        p = Path(self._settings["root_path"])
        for q in p.glob('config/*.toml'):
            with q.open() as f:
                name, config = q.stem, toml.loads(f.read())
                # app.toml 为全局配置文件，但是优先级低于 Application 初始化时候的参数
                if name != "app":
                    self._config_file_cache[name] = config
                    continue
                config.update(self._settings)
                self._settings = config

    def __getattr__(self, key):
        """settings 获取的优先级，首先从 _settings 里面选择，如果不是字典则直接返回
        然后再从 config 文件夹中的缓存获取 里面寻找，如果是字典类型的话和之前的结果进行合并然后返回
        否则都没有的话，返回None
        """
        if key.startswith("_"):
            return self.__dict__[key]
        _setting = self._settings.get(key, None)
        if _setting is not None and type(_setting) is not dict:
            return deepcopy(_setting)
        cached_setting = self._config_file_cache.get(key, None)
        if cached_setting is None or _setting is None:
            return deepcopy(cached_setting or _setting)
        r = deepcopy(cached_setting)
        r.update(_setting)
        return r

    def __setattr__(self, key, value):
        """所有的设置只能通过这里修改，支持使用通过使用.来修改字典类型
        app.settings["database.host"] = "dev.local"
        """
        if key.startswith("_"):
            self.__dict__[key] = value
        keys = key.split(".")
        m = {keys.pop(): value}
        if len(keys) is not 0:
            keys.sort(reverse=True)
            for k in keys:
                m = {k: m}
        self._settings.update(m)

    __getitem__ = __getattr__
    __setitem__ = __setattr__


class HttpRequestHandler(ServerHttpProtocol):

    @asyncio.coroutine
    def handle_request(self, message, payload):
        response = Response(
            self.writer, 200, http_version=message.version
        )
        response.add_header('Content-Type', 'text/html')
        response.add_header('Content-Length', '18')
        response.send_headers()
        response.write(b'<h1>It Works!</h1>')
        yield from response.write_eof()


class Application(object):

    def __init__(self, **kwargs):
        self.loop = asyncio.get_event_loop()
        self.srv = None
        self.settings = Settings(**kwargs)

    @asyncio.coroutine
    def _register_provider(self):
        for p in self.settings.bootstrap["providers"]:
            m = dynamic_import((None, "apostles"), "providers", p)
            clsmembers = inspect.getmembers(m, inspect.isclass)
            for _, cls in clsmembers:
                if not issubclass(cls, Provider) or cls is Provider:
                    continue
                assert asyncio.iscoroutinefunction(cls.register)
                yield from cls.register(self)

    # @asyncio.coroutine
    def create_server(self, host, port, keep_alive):
        # 载入所有的 providers
        self.loop.create_task(self._register_provider())
        coro = self.loop.create_server(
            lambda: HttpRequestHandler(
                debug=self.settings.env != "production",
                keep_alive=keep_alive
            ), host, port)
        self.srv = self.loop.run_until_complete(coro)

    def run(self, host="0.0.0.0", port=7890, keep_alive=75):
        self.create_server(host, port, keep_alive)
        print('Serving on', self.srv.sockets[0].getsockname())
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            exit(0)
