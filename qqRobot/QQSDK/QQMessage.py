#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-08 15:27:06
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://bitwater1997.cn
# @Version : $Id$

'''
    "from_uin": 3785096088,
    "msg_id": 25477,
    ##"msg_type": 0,
    "time": 1450686775,
    "to_uin": 931996776

群消息
    "from_uin": 2323421101,
    "group_code": 2323421101,
    "msg_id": 50873,
    "msg_type": 0,
    "send_uin": 3680220215,
    "time": 1450687625,
    "to_uin": 931996776

讨论组
    "from_uin": 2322423201,
    "did": 2322423201,
    "msg_id": 50873,
    "msg_type": 0,
    "send_uin": 3680220215,
    "time": 1450687625,
    "to_uin": 931996776
'''


class QQMessage(object):
    """docstring for  QQMessage"""
    PERSION_MESSAGE = 'message'
    GROUP_MESSAGE = 'group_message'
    DISCUSS_MESSAGE = 'discu_message'

    def __init__(self, poll_type, content, from_uin, to_uin, send_uin=None, group_code=None, did=None, msg_id=None, time=None):
        self.message_type = poll_type
        self.content = content
        self.from_uin = from_uin
        self.to_uin = to_uin
        self.send_uin = send_uin
        self.group_code = group_code
        self.msg_id = msg_id
        self.did = did
        self.time = time
        self.reply = None

    def __str__(self):

        if self.message_type == QQMessage.PERSION_MESSAGE:
            return "%s ---%s : %s" % (self.message_type, self.from_uin, self.content)
        else:
            return "%s ---%s(in(%s)) : %s" % (self.message_type, self.from_uin, self.send_uin, self.content)
