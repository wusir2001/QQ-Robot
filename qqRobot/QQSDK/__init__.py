#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-08 15:19:41
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://bitwater1997.cn
# @Version : $Id$

import os
import logging
import logging.config

log_file_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'logging_config.ini')
logging.config.fileConfig(log_file_path)
logger = logging.logger = logging.getLogger('QQSDK')


from .QQClient import QQClient
from .QQMessage import QQMessage
from .QQError import QQError
