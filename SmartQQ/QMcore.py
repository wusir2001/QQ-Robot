#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 17:54:42
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : 1.0

from .QMconfig import QRcode_path
from .QMsession import QMsession
from .tuling import TulingSDK
from .QMdialmessage import QMdialmessage
from .QMsocket import QMsocket
from .QMlog import Warning, Error, Info
from .QMhistory import QMhistory


class QMcore(object):

    def __init__(self, APIkey):
        self.tuling = TulingSDK(APIkey)
        self.qmsession = QMsession()
        self.qmsocket = QMsocket(QRcode_path)
        self.qmhistory = QMhistory()

    def start(self):
        self.qmhistory.clear()
        self.qmsocket.start()
        self.qmsession.login()
        self.nick, self.qq = self.qmsession.get_info()
        self.qmhistory.save_admin(user_name=self.nick, user_qq=self.qq)

        self.save_friends()
        self.mainloop()

    def mainloop(self):
        while True:
            message = self.qmsession.get_message()

            if not message:
                continue

            Info(message.content)

            if message.message_type == QMdialmessage.PERSION_MESSAGE:
                message.reply = str(self.tuling.talk(message.content).content)
                self.qmsession.send_message_to_persion(message)
                self.save_chat_message(message)
            else:
                ata = '@%s' % (self.nick)
                if ata in message.content:
                    cont = "".join(message.content.split(ata))
                    Info(cont)
                    message.reply = str(self.tuling.talk(cont).text)
                    if message.message_type == QMdialmessage.GROUP_MESSAGE:
                        self.qmsession.send_message_to_group(message)
                    elif message.message_type == QMdialmessage.DISCUSS_MESSAGE:
                        self.qmsession.send_message_to_discuss(message)

    def save_chat_message(self, message):
        # Info(message)
        user = self.qmhistory.get_user_info(message.from_uin)
        self.qmhistory.save_chat_message(user_name=self.nick, user_qq=self.qq,
                                         message_type=message.message_type, from_name=user.user_name,
                                         from_qq=user.user_qq, from_text=message.content, reply_text=message.reply)

    def save_friends(self):
        Info('start to save_friends')
        info, marknames = self.qmsession.get_user_friends()
        friends = []
        for i in info:
            tmp = [i['uin'], i['nick'], '', '']
            for mk in marknames:
                if i['uin'] == mk['uin']:
                    tmp[2] = mk['markname']
                    break
            tmp[3] = self.qmsession.get_qq_nub(i['uin'])
            Info(str(tmp))
            friends.append(tmp)
        self.qmhistory.save_friends(friends)
