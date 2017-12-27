#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-20 11:35:02
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://bitwater1997.cn
# @Version : $Id$

from . import app
from MQSDK import MQmsg
from .config import tuling_APIkey ,baiduTran_SECRET,baiduTran_APIID
from tulingBot import TulingAPI
from .control import  TransAPI




@app.msg_route('menu',is_listen=True)
@app.deal_other_message
def menu_lis(msg):
    return '功能菜单\n1. 翻译()输入tran 语句\n2. 作者 输入author'

@app.msg_route('^tran.+',is_listen=True)
@app.deal_other_message
def tran_lis(msg):
    text = msg.content.replace('tran', '')
    api = TransAPI(baiduTran_APIID, baiduTran_SECRET)
    return api.tran(text=text, _to='zh')


@app.msg_route('menu|@.+menu')
@app.deal_to_me_message
def menu(msg):
    app.logger.info("消息处理(author)")
    return '功能菜单\n1. 翻译()输入tran 语句\n2. 作者 输入author'


@app.msg_route('author|@.+author')
@app.deal_to_me_message
def author(msg):
    app.logger.info("消息处理(author)")
    return 'bitwater'

@app.msg_route('^tran.+|@.+tran.+')
@app.deal_to_me_message
def tran(msg):
    app.logger.info("消息处理(tran)")
    text = msg.content.replace('tran','')
    api = TransAPI(baiduTran_APIID, baiduTran_SECRET)
    return api.tran(text=text, _to='zh')


@app.msg_route(is_default=True)
@app.deal_to_me_message
def msg_default(msg):
    app.logger.info("消息处理(default)")
    tuling = TulingAPI(tuling_APIkey)
    return tuling.talk(msg.content).content




