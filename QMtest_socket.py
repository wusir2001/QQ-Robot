#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-05 11:28:16
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : $Id$

from SmartQQ.QMsocket import QMsocket

if __name__ == '__main__':
    qs = QMsocket(QRcode_path="SmartQQ/QRcode/QRcode.jpg")
    qs.start()
