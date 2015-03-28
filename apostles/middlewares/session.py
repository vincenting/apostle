#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-28 17:17:20
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

from abc import abstractmethod

from .abc import MiddleWare


class SessionStore(object):

    @abstractmethod
    def get():
        pass

    @abstractmethod
    def set():
        pass
