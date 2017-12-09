#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-08 16:24:38
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://bitwater1997.cn
# @Version : $Id$


class QQError(BaseException):
    def __init__(self, error_code, error, http_code=None):

        self.error = error
        self.error_code = error_code
        self.http_code = http_code

    def __str__(self):
        return 'http_code : %s\nerror_code : %s\nerror : %s\n' % (
            self.http_code,
            self.error,
            self.error_code,
            self.request)