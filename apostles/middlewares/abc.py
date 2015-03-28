#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-28 17:09:31
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

from abc import abstractmethod


class MiddleWare(object):

    @abstractmethod
    def enter(req, res, app):
        """请求开始的时候执行的函数
        如果最终返回 False 则请求结束，不会继续执行下去
        """

    @abstractmethod
    def exit(req, res, app):
        """在执行 res.finish() 之前执行的内容
        就算 enter 返回 False 这里也会被执行
        """
