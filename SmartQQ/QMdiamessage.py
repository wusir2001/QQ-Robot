#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-11 23:08:14
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : 1.0


'''
    "from_uin": 3785096088,
    "msg_id": 25477,
    "msg_type": 0,
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


class QMdialmessage(object):
    """docstring for  QMdialmessage"""
    DISCUSS = 2
    GROUP = 1
    PERSION = 0

    def __init__(self, dia_type, content, from_uin, to_uin, send_uin=None, group_code=None, msg_id=None, msg_type=None, time=None):
        self.dia_type = dia_type
        self.content = content
        self.from_uin = from_uin
        self.to_uin = to_uin
        self.send_uin = send_uin
        self.group_code = group_code
        self.msg_type = msg_type
        self.msg_id = msg_id
        self.time = time

    def __str__(self):
        return "%s : %s ;to(%s)(type:%s)" % (self.from_uin, self.content, self.to_uin, self.poll_type)

    __repr__ = __str__
