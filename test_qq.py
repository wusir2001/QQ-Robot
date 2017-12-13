#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-30 09:34:07
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : $Id$s

from qqRobot import Botcore
from config import APIkey
import os
import logging
import logging.config

log_file_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'logging_config.ini')
logging.config.fileConfig(log_file_path)
logger = logging.logger = logging.getLogger('qqrobot')

if __name__ == '__main__':

    bot = Botcore(APIkey, 'qrcode.jpg')
    bot.start()
