#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-30 09:34:07
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : $Id$s

from qqRobot import Botcore
from config import APIkey

if __name__ == '__main__':

    bot = Botcore(APIkey)
    bot.start()
