#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-09 17:35:15
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://bitwater1997.cn
# @Version : $Id$

from QQSDK.QQClient import QQClient

if __name__ == '__main__':
    qq = QQClient()
    qq.login()
    # print (qq.get_user_friends())
    while True:
        msg = qq.get_message()
        print(msg)
