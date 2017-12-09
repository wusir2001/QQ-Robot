#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-13 20:24:28
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : 1.0

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# QRcode
QRcode_path = os.path.join(basedir, "QRcode/QRcode.jpg")

# datebase
Datebase_path = 'sqlite:///' + \
    os.path.join(basedir, 'database/app.db')
