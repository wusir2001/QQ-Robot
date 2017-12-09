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

    def __init__(self, APIkey):
        self.tuling = TulingSDK(APIkey)
        self.qqclient = QQClient()
        self.hist = Bothistory()
        self.logger = logging.getLogger('qqRobot.Botcore')

    def start(self):
        Botsocket('qrcode.jpg').start()
        self.qqclient.login()
        self.hist.clear()
        self.hist.save_admin(
            user_name=self.qqclient.qquser.nick, user_qq=self.qqclient.qquser.qq)

        self.save_friends()
        self.mainloop()

    def mainloop(self):
        while True:
            message = self.qqclient.get_message()
            self.logger.info('get message :%s', message)
            if message is None:
                continue
            if message.message_type == QQMessage.PERSION_MESSAGE:
                message.reply = self.tuling.talk(message.content).content
                self.logger.info('reply : %s', message.reply)

                self.save_chat_message(message)

                try:
                    self.qqclient.send_message_to_persion(message)
                except QQError.QQError as e:
                    self.logger.error('send message fail \n%s', str(e))
            else:
                ata_me = '@%s' % (self.qqclient.qquser.nick)
                if ata_me in message.content:
                    cont = "".join(message.content.split(ata_me))
                    message.reply = self.tuling.talk(cont).content
                    self.logger.info('reply : %s', message.reply)

                    self.save_chat_message(message)

                    if message.message_type == QQMessage.GROUP_MESSAGE:
                        try:
                            self.qqclient.send_message_to_group(message)
                        except QQError.QQError as e:
                            self.logger.error('send message fail \n%s', str(e))

                    elif message.message_type == QQMessage.DISCUSS_MESSAGE:
                        try:
                            self.qqclient.send_message_to_discuss(message)
                        except QQError.QQError as e:
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

    def save_friends(self):
        self.logger.info('start to save_friends')
        info, marknames = self.qqclient.get_user_friends()
        friends = []
        for i in info:
            tmp = [i['uin'], i['nick'], '', '']
            for mk in marknames:
                if i['uin'] == mk['uin']:
                    tmp[2] = mk['markname']
                    break
            tmp[3] = self.qqclient.get_qq_nub_from_uin(i['uin'])
            self.logger.info(str(tmp))
            friends.append(tmp)
        self.hist.save_friends(friends)
