#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-13 19:53:09
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : 1.0

import os
import logging
import logging.config

log_file_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'logging_config.ini')
logging.config.fileConfig(log_file_path)
logger = logging.logger = logging.getLogger(__name__)


Warning = logger.warning
Error = logger.error
Info = logger.info