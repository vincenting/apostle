#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-28 19:03:04
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

__all__ = ("Provider")

from abc import abstractmethod


class Provider(object):

    @staticmethod
    @abstractmethod
    def register(application):
        """将当前 provider 注册到 Application 实例中
        """
