#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2015-03-29 14:10:32
# @Author  : Vincent Ting (homerdd@gmail.com)
# @Link    : http://vincenting.com

import site
from os import path

site.addsitedir(path.realpath("../../"))


from apostles.web import Application

if __name__ == "__main__":
    app = Application()
    app.run()
