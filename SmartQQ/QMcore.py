#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 17:54:42
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : 1.0

from .QMsession import QMsession
from .tuling import TulingSDK
from .QMdialmessage import QMdialmessage
from .QMlog import Warning, Error, Info


class QMcore(object):

    def __init__(self, APIkey):
        self.tuling = TulingSDK(APIkey)
        self.qmsession = QMsession()

    def login(self):
        self.qmsession.login()

    def mainloop(self):
        while True:
            message = self.qmsession.get_message()

            if not message:
                continue
            message.reply = str(self.tuling.talk(message.content).text)
            if message.message_type == QMdialmessage.PERSION_MESSAGE:
                self.qmsession.send_message_to_persion(message)

            elif message.message_type == QMdialmessage.GROUP_MESSAGE:
                pass
                # self.qmsession.send_message_to_group(message)
            elif message.message_type == QMdialmessage.DISCUSS_MESSAGE:
                pass
            self.qmsession.send_message_to_discuss(message)
