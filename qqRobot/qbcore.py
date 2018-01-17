#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 17:54:42
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : 1.0

import time
import logging
from MQSDK import MQAPI, MQerr, MQmsg
import re


class qbcore(object):

    def __init__(self, qrpath=None, username=None, password=None, is_show=True):

        self.__qqclient = MQAPI()
        self.logger = logging.getLogger('qqRobot.Botcore')

        # 认证方式设置
        self.__qrpath = qrpath
        self.__username = username
        self.__password = password
        self.__is_show = is_show



        self.__listen_routes = []   # 监听消息列表

        self.__msg_routes = {}      # 消息内容处理路由
        self.__msg_default = None   # 默认处理消息


        # 运行状态统计
        self.init_time = time.time()
        self.login_cnt = 0
        self.login_time = None
        self.send_cnt = 0

        # 群相关
        self.groups_list = {}       # 群名称做索引
        self.groups_info = {}       # 群code 做索引
        self.groups_mem = {}        # 群code 做索引
        self.friends_list = {}      # 好友列表 uin 做索引



    def login_by_qrcode(self):
        self.__qqclient.login_by_qrcode(self.__qrpath)

    def login_by_pass(self):
        self.__qqclient.login_by_pass(self.__username, self.__password, self.__is_show)

    def start(self):
        self.login_cnt += 1
        self.login_time = time.time()
        self.__qqclient.logout()
        if self.__qrpath:
            self.login_by_qrcode()
        else:
            self.login_by_pass()

        self.uin = self.__qqclient.uin
        self.qq = self.__qqclient.qq
        self.nick = self.__qqclient.nick

        self.friends_list = self.__qqclient.get_user_friends2()
        self.groups_list = self.__qqclient.get_group_name_list_mask2()
        # self.__discus_list = self.__qqclient.get_discus_list()

        self.mainloop()

    # 注册监听函数
    def listen_route(self):
        def wrap(f):
            self.__listen_routes.append(f)
        return wrap

    # 注册消息处理路由
    def msg_route(self, path=None, is_default=False):
        def wrap(f):
            if is_default:
                self.__msg_default = f
            else:
                self.__msg_routes[path] = f

        return wrap

    # 主循环
    def mainloop(self):
        cnt = 0
        while True:
            cnt += 1
            if cnt > 8888:
                raise Exception("重新登入")

            msg = self.__qqclient.poll2()
            if msg:
                self.logger.info('get message :%s', msg)
                self.__deal_message(msg)

    def __deal_message(self, msg):
        #  不处理自己发送的
        if msg.from_uin == self.uin or msg.send_uin == self.uin:
            return

        self.logger.info("开始处理消息")

        # 先处理监听事件
        for f in self.__listen_routes:
            f(msg)

        for key in self.__msg_routes:
            if re.match(key, msg.content):
                self.__msg_routes[key](msg)
                return
        self.logger.info("默认回复消息")
        if self.__msg_default:
            self.__msg_default(msg)

    def send_buddy(self, msg):
        self.send_cnt += 1
        self.__qqclient.send_buddy_msg2(msg.from_uin, msg.reply)

    def send_group(self, msg):
        self.send_cnt += 1
        self.__qqclient.send_qun_msg2(msg.group_code, msg.reply)

    def send_discs(self, msg):
        self.send_cnt += 1
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
            else:
                at_me = '@%s' % self.nick
                if at_me in msg.content:
                    msg.content = msg.content.replace(at_me, '')
                    msg.reply = f(msg)
                    self.send_all(msg)

        return wrapper

    def deal_other_message(self, f):
        def wrapper(msg):
            at_me = '@%s' % self.nick
            if msg.poll_type != MQmsg.PERSION_MESSAGE and at_me not in msg.content:
                msg.reply = f(msg)
                self.send_all(msg)

        return wrapper

    def get_group_info(self, gname):
        if gname not in self.groups_list:
            self.logger.warning("not find qq group(%s)", gname)
            return None
        code = self.groups_list[gname]['code']
        if code in self.groups_info:
            return self.groups_info[code], self.groups_mem[code]

        ginfo, minfo = self.__qqclient.get_group_info_ext2(code)
        self.groups_info[code] = ginfo
        self.groups_mem[code] = minfo
        return ginfo, minfo
