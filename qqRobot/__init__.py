#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-07 09:27:01
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : 1.0

import sys
import os
import logging
import logging.config
from .config import username, password, tuling_path, smartqq_sdk_path, qr_path
sys.path.append(smartqq_sdk_path)
sys.path.append(tuling_path)

log_file_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'logging_config.ini')
logging.config.fileConfig(log_file_path)
logger = logging.logger = logging.getLogger('qqrobot')

from .qbcore import qbcore

app = qbcore()
app.config(username=username, password=password, qr_path=qr_path)
from .view import *
