#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 17:54:42
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : 1.0


import logging
from MQSDK import MQAPI, MQerr, MQmsg
import re


class qbcore(object):

    def __init__(self,qrpath = None, username = None,password = None,is_show = True):

        self.__qqclient = MQAPI()
        self.logger = logging.getLogger('qqRobot.Botcore')

        self.__qrpath = qrpath
        self.__username = username
        self.__password = password
        self.__is_show = is_show

        self.__deal_routes = {}
        self.__msg_default = None

    def login_by_qrcode(self):
        self.__qqclient.login_by_qrcode(self.__qr_path)

    def login_by_pass(self):
        self.__qqclient.login_by_pass(self.__username, self.__password, self.__is_show)

    def start(self):
        self.__qqclient.logout()
        if self.__qrpath :
            self.login_by_qrcode()
        else:
            self.login_by_pass()

        self.uin = self.__qqclient.uin
        self.qq = self.__qqclient.qq
        self.nick = self.__qqclient.nick

        self.__friend_list = self.__qqclient.get_user_friends2()
        self.__group_list = self.__qqclient.get_group_name_list_mask2()
        self.__discus_list = self.__qqclient.get_discus_list()

        self.mainloop()

    def msg_route(self, path=None, is_default=False):
        def wrap(f):
            if is_default:
                self.__msg_default = f
            else:
                self.__deal_routes[path] = f

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
        if msg is None or msg.from_uin == self.uin or msg.send_uin == self.uin:
            return

        self.logger.info('开始处理消息')

        for key in self.__deal_routes:
            if re.match(key, msg.content):
                self.__deal_routes[key](msg)
                return
        self.logger.info('处理默认消息')

        if self.__msg_default:
            self.__msg_default(msg)

    def send_buddy(self, msg):
        self.__qqclient.send_buddy_msg2(msg.from_uin, msg.reply)

    def send_group(self, msg):
        self.__qqclient.send_qun_msg2(msg.group_code, msg.reply)

    def send_discs(self, msg):
        self.__qqclient.send_discu_msg2(msg.did, msg.reply)

    def send_all(self, msg):
        self.logger.info('开始回复消息')
        if msg.poll_type == MQmsg.PERSION_MESSAGE:
            self.send_buddy(msg)
        else:
            if msg.poll_type == MQmsg.GROUP_MESSAGE:
                self.send_group(msg)
            elif msg.poll_type == MQmsg.DISCUSS_MESSAGE:
                self.send_discs(msg)

    def deal_to_me_message(self, f):
        def wrapper(msg):
            if msg.poll_type == MQmsg.PERSION_MESSAGE:
                msg.reply = f(msg)
                self.send_all(msg)
                return True
            else:
                at_me = '@%s' % self.nick
                if at_me in msg.content:
                    cont = msg.content.replace(at_me, '')
                    msg.reply = f(cont)
                    self.send_all(msg)
                    return True
                return False

        return wrapper

    def deal_other_message(self, f):
        def wrapper(msg):
            if msg.poll_type == MQmsg.PERSION_MESSAGE:
                return
            else:
                at_me = '@%s' % self.nick
                if at_me in msg.content:
                    return
                msg.reply = f(msg)
                self.send_all(msg)

        return wrapper
