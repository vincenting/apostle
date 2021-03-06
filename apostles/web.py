#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-28 16:56:17
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import asyncio
import inspect
import toml
import os
import importlib
from pathlib import Path
from copy import deepcopy

from .utils import SingletonDecorator
from .providers.abc import Provider

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


@asyncio.coroutine
def default_handler(r, w):
    pass


class Application(object):

    def __init__(self, **kwargs):
        self.loop = asyncio.get_event_loop()
        self.srv = None
        self.settings = Settings(**kwargs)

    def import_vendor(self, package, name):
        return dynamic_import((None, "apostles"), package, name)

    @asyncio.coroutine
    def _register_provider(self):
        for p in self.settings.bootstrap["providers"]:
            m = self.import_vendor("providers", p)
            clsmembers = inspect.getmembers(m, inspect.isclass)
            for _, cls in clsmembers:
                if not issubclass(cls, Provider) or cls is Provider:
                    continue
                cls.register(self)

    def create_server(self, host, port, **kwargs):
        # 载入所有的 providers
        # TODO 这里存在 BUG，start_server 会在 _register_provider 前执行，考虑使用锁
        self._register_provider()
        coro = asyncio.start_server(
            # 允许通过 settings.handler 修改默认的 HTTP 请求处理
            # 当然，这里如果可以的话，可以变成各种协议
            self.settings["handler"] or default_handler,
            host=host,
            port=port,
            loop=self.loop,
            **kwargs
        )
        self.srv = self.loop.run_until_complete(coro)

    def run(self, host="0.0.0.0", port=7890, **kwargs):
        self.create_server(host, port, **kwargs)
        print('Serving on', self.srv.sockets[0].getsockname())
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            exit(0)
