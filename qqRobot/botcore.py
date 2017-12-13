#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 17:54:42
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : 1.0


import logging
from .QQSDK import QQClient, QQMessage, QQError
from .tuling import TulingSDK
from .bothistory import Bothistory
from .botsocket import Botsocket


class Botcore(object):

    def __init__(self, APIkey, qr_path):
        self.qr_path = qr_path
        self.tuling = TulingSDK(APIkey)
        self.qqclient = QQClient(qr_path)
        self.hist = Bothistory()
        self.logger = logging.getLogger('qqRobot.Botcore')

    def start(self):
        Botsocket(self.qr_path).start()
        self.qqclient.login()

        self.hist.clear()
        self.hist.save_admin(self.qqclient.qquser.qq,
                             self.qqclient.qquser.nick)
        self.hist.save_friends(self.qqclient.get_friend_list())
        self.hist.save_groups(self.qqclient.get_group_list())
        self.hist.save_discuss(self.qqclient.get_discus_list())

        self.mainloop()

    def mainloop(self):
        while True:

            try:
                message = self.qqclient.get_message()
            except QQError:
                self.logger.info('出现错误,尝试重新登录')
                self.qqclient.login()
                continue
            self.logger.info('get message :%s', message)
            if message is None:
                continue
            if message.message_type == QQMessage.PERSION_MESSAGE:
                message.reply = self.tuling.talk(message.content).content

                self.save_chat_message(message)

                try:
                    self.qqclient.send_message_to_persion(
                        message.reply, message.from_uin)
                except QQError as e:
                    self.logger.error('send message fail \n%s', str(e))
            else:
                ata_me = '@%s' % (self.qqclient.qquser.nick)
                if ata_me in message.content:
                    cont = "".join(message.content.split(ata_me))
                    message.reply = self.tuling.talk(cont).content

                    self.save_chat_message(message)

                    if message.message_type == QQMessage.GROUP_MESSAGE:
                        try:
                            self.qqclient.send_message_to_group(
                                message.reply, message.group_code)
                        except QQError as e:
                            self.logger.error('send message fail \n%s', str(e))

                    elif message.message_type == QQMessage.DISCUSS_MESSAGE:
                        try:
                            self.qqclient.send_message_to_discuss(
                                message.reply, message.did)
                        except QQError as e:
                            self.logger.error('send message fail \n%s', str(e))

    def save_chat_message(self, message):
        uin = message.from_uin
        if message.message_type != QQMessage.PERSION_MESSAGE:
            uin = message.send_uin
        user = self.hist.get_user_info_from_uin(str(uin))
        if user is None:
            self.logger.info("can't find user uin:%s", uin)
            return
        self.logger.info('get message from user_info\n%s', str(user))
        self.hist.save_chat_message(user_name=self.qqclient.qquser.nick, user_qq=self.qqclient.qquser.qq,
                                    message_type=message.message_type, from_name=user.user_name,
                                    from_qq=user.user_qq, from_text=message.content, reply_text=message.reply)
