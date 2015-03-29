#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-29 11:19:41
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

from apostles.web import Settings
from .utils import CURRENT_PATH

settings = Settings(root_path=CURRENT_PATH)


def test_settings_init():
    assert len(settings._config_file_cache) > 0


def test_get_from_toml():
    assert type(settings.bootstrap["commands"]) is list


def test_update_toml_config():
    settings["bootstrap.middlewares"] = False
    settings.bootstrap["middlewares"] = True
    assert settings.bootstrap["middlewares"] is False


def test_set_and_get():
    settings.name = "vincent"
    assert settings.name == "vincent"
