#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 17:54:42
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : 1.0


import logging
from MQSDK import MQAPI, MQerr
import re


class qbcore(object):

    def __init__(self):

        self.__qqclient = MQAPI()
        self.logger = logging.getLogger('qqRobot.Botcore')

        self.__routes = {}
        self.__msg_default = None

    def config(self, qr_path=None, username=None, password=None):
        self.__qr_path = qr_path
        self.__username = username
        self.__password = password

    def login(self):
        if self.__qr_path:
            self.__qqclient.login_by_qrcode(self.__qr_path)
        else:
            self.__qqclient.login_by_pass(self.__username, self.__password)
        self.uin = self.__qqclient.uin
        self.qq = self.__qqclient.qq
        self.nick = self.__qqclient.nick

    def start(self):
        self.login()
        info = self.__qqclient.get_self_info2()
        print (info)
        self.__friend_list = self.__qqclient.get_user_friends2()
        self.__group_list = self.__qqclient.get_group_name_list_mask2()
        self.__discus_list = self.__qqclient.get_discus_list()

        self.mainloop()

    def msg_route(self, path=None, is_default=False):
        def wrap(f):
            if is_default:
                self.__msg_default = f
            else:
                self.__routes[path] = f
        return wrap

    def mainloop(self):
        while True:
            try:
                msg = self.__qqclient.poll2()
            except MQerr:
                self.logger.info('出现错误,尝试重新登录')
                self.login()
                continue
            self.logger.info('get message :%s', msg)
            self.__deal_message(msg)

    def __deal_message(self, msg):
        if msg is None:
            return
        for key in self.__routes:
            if re.match(key, msg.content):
                self.__routes[key](msg)
                return
        self.__msg_default(msg)

    def send_buddy(self, msg):
        self.__qqclient.send_buddy_msg2(msg.from_uin, msg.reply)

    def send_group(self, msg):
        self.__qqclient.send_qun_msg2(msg.group_code, msg.reply)

    def send_discs(self, msg):
        self.__qqclient.send_discu_msg2(msg.did, msg.reply)
