#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 17:54:42
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : 1.0

from .QMsession import QMsession
from .tuling import TulingSDK


class QMcore(object):

    def __init__(self, APIkey):
        self.tuling = TulingSDK(APIkey)
        self.qmsession = QMsession()

    def login(self):
        self.qmsession.login()

    def mainloop(self):
        while True:
            message_type, uid, message = self.qmsession.get_message()
            replay = self.tuling.talk(message)
            self.qmsession.send_message(message_type, uid, replay)
