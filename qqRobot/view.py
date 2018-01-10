#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-20 11:35:02
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://bitwater1997.cn
# @Version : $Id$


from . import app
from qqRobot.config import tuling_APIkey, baiduTran_SECRET, baiduTran_APIID
from tulingBot import TulingAPI
from MQSDK import MQAPI, MQerr, MQmsg
from .control import TransAPI, Exin
import time

exin = Exin()


@app.listen_route()
def exin_sb(msg):
    uin = msg.send_uin if msg.send_uin else msg.from_uin
    content = exin.isMatch(uin)
    if content:
        msg.reply = content
        app.send_all(msg)


@app.msg_route('fuck.+')
def fuck(msg):
    '''
    隐藏命令, 只处理私聊的
    命令格式 :
        fuck$昵称/备注$语句
    效果:
        每次他在群里发言 @他(优先备注)回复他一句话
    '''
    app.logger.info("消息处理(fuck)")
    if msg.poll_type == MQmsg.PERSION_MESSAGE:
        cmd = msg.content.split("$")
        if len(cmd) == 3:
            for f in app.friends_list:
                if app.friends_list[f]['markname'] == cmd[1] or \
                        app.friends_list[f]['nick'] == cmd[1]:

                    app.logger.info("fuck (%s,%s,%s)", cmd[1], f, cmd[2])
                    # 判断删除还是增加
                    if cmd[2] == '-r':
                        c = exin.remove(f)
                        msg.reply = '删除 uin:%s,%s' % (f,c)
                    else:
                        exin.set(f, cmd[2])
                        msg.reply = '成功 uin:%s' % (f)
            if not msg.reply:
                msg.reply = '未找到此人'
        else :
            msg.reply = '命令格式不正确\n命令格式:fuck$昵称/备注$-r(删除)/语句'
        app.send_all(msg)

@app.msg_route('status')
def status(msg):
    '''
    显示qq运行状态
    全局命令 不需要@
    '''
    app.logger.info("消息处理(status)")

    msg.reply = "初始化时间:%s\n登入次数:%d\n本次登入时间:%s\n回复消息条数:%d\n" % (
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(app.init_time)),
        app.login_cnt,
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(app.login_time)),
        app.send_cnt
    )
    app.send_all(msg)


@app.msg_route('menu')
def menu(msg):
    '''
    显示菜单
    全局命令 不需要@
    '''
    app.logger.info("消息处理(author)")
    msg.reply = '功能菜单\n1. 翻译功能: 输入tran+语句\n2. 作者:输入author'
    app.send_all(msg)


@app.msg_route('author|@.+author')
@app.deal_to_me_message
def author(msg):
    '''
    显示作者, 只处理与我交互的
    '''
    app.logger.info("消息处理(author)")
    return 'bitwater'


@app.msg_route('^tran.+')
def tran(msg):
    '''
    翻译句子, 全局命令
    :param msg:
    :return:
    '''
    app.logger.info("消息处理(tran)")
    text = msg.content.replace('tran', '')
    api = TransAPI(baiduTran_APIID, baiduTran_SECRET)
    try:
        msg.reply = api.tran(text=text, _to='zh')
    except:
        msg.reply = "there is some error in api"
    app.send_all(msg)


@app.msg_route(is_default=True)
@app.deal_to_me_message
def msg_default(msg):
    '''
    默认消息处理 , 当然只处理与我交互的
    '''
    app.logger.info("消息处理(default)")
    tuling = TulingAPI(tuling_APIkey)
    return tuling.talk(msg.content).content
