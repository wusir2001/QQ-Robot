#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-20 11:35:02
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://bitwater1997.cn
# @Version : $Id$

from . import app
from MQSDK import MQmsg
from .config import APIkey
from TulingSDK import TulingAPI


@app.msg_route('author|作者')
def name(msg):
    if msg.poll_type == MQmsg.PERSION_MESSAGE:
        msg.reply = 'bitwater'
        app.send_buddy(msg)


@app.msg_route(is_default=True)
def msg_default(msg):
    tuling = TulingAPI(APIkey)
    if msg is None:
        return
    if msg.poll_type == MQmsg.PERSION_MESSAGE:
        msg.reply = tuling.talk(msg.content).content
        app.send_buddy(msg)
    else:
        at_me = '@%s' % (app.nick)
        if at_me in msg.content:
            cont = "".join(msg.content.split(at_me))
            msg.reply = tuling.talk(cont).content
            if msg.msg_type == MQmsg.GROUP_MESSAGE:
                app.send_group(msg)
            elif msg.msg_type == MQmsg.DISCUSS_MESSAGE:
                app.send_discs(msg)
