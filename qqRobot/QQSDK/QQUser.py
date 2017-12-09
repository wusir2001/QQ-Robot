#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-08 15:25:15
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://bitwater1997.cn
# @Version : $Id$

import time
import logging
import os
from .QQUtils import bknHash, qHash
import random
import codecs
from .QQError import QQError
import json


class QQUser(object):
    """docstring for QQUser"""

    def __init__(self, qqsession, clientid):
        self.clientid = clientid
        self.qqsession = qqsession
        self.logger = logging.getLogger('QQSDK.QQUser')

        self.ptwebqq = None
        self.vfwebqq = None
        self.psessionid = None
        self.uin = None

        self.nick = None
        self.qq = None

    def login(self):

        self.logger.info('start __get_auth_status')
        self.__get_auth_status()

        self.qqsession.session.cookies.pop('qrsig')

        self.logger.info('start __wait_auth')
        self.__wait_auth()

        self.logger.info('start __get_Ptwebqq')
        self.__get_Ptwebqq()

        self.logger.info('start __get_Vfwebqq')
        self.__get_Vfwebqq()

        self.logger.info('start __get_UinAndPsessionid')
        self.__get_UinAndPsessionid()

        self.__get_info()

    def __show_QRcode(self):
        qrcode = self.qqsession.get_url(
            'https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=0&l=M&' +
            's=5&d=72&v=4&t=' + repr(random.random())
        ).content
        qrdir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), '../../qrcode.jpg')
        with codecs.open(qrdir, 'wb') as f:
            f.write(qrcode)

    def __get_auth_status(self):

        result = self.qqsession.get_url(
            url='https://ssl.ptlogin2.qq.com/ptqrlogin?ptqrtoken=' +
                str(bknHash(self.qqsession.session.cookies['qrsig'], init_str=0)) +
                '&webqq_type=10&remember_uin=1&login2qq=1&aid=501004106' +
                '&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26' +
                'webqq_type%3D10&ptredirect=0&ptlang=2052&daid=164&' +
                'from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-' +
                repr(random.random() * 900000 + 1000000) +
                '&mibao_css=m_webqq&t=undefined&g=1&js_type=0' +
                '&js_ver=10141&login_sig=&pt_randsalt=0',
            Referer=('https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&'
                     'target=self&style=16&mibao_css=m_webqq&appid=501004106&'
                     'enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2F'
                     'w.qq.com%2Fproxy.html&f_url=loginerroralert&'
                     'strong_login=1&login_state=10&t=20131024001')
        ).content
        return result

    def __wait_auth(self):
        self.__show_QRcode()
        while True:
            time.sleep(3)
            authStatus = self.__get_auth_status().decode('utf-8')
            if '二维码未失效' in authStatus:
                self.logger.info('等待二维码扫描及授权...')
            elif '二维码认证中' in authStatus:
                self.logger.info('二维码已扫描，等待授权...')
            elif '二维码已失效' in authStatus:
                self.logger.warning('二维码已失效, 重新获取二维码')
                self._show_QRcode()
            elif '登录成功' in authStatus:
                self.logger.info('已获授权')
                items = authStatus.split(',')
                self.nick = str(items[-1].split("'")[1])
                self.qq = str(
                    int(self.qqsession.session.cookies['superuin'][1:]))
                self.urlPtwebqq = items[2].strip().strip("'")
                break
            else:
                self.logger.error('获取二维码扫描状态时出错, html="%s"' % (authStatus))
                raise QQError('0001', authStatus)

    def __get_Ptwebqq(self):
        self.qqsession.get_url(self.urlPtwebqq)
        self.ptwebqq = self.qqsession.session.cookies['ptwebqq']
        self.logger.info('已获取ptwebqq')

    def __get_Vfwebqq(self):
        self.vfwebqq = self.qqsession.smartQQ_request(
            url=('http://s.web2.qq.com/api/getvfwebqq?ptwebqq=%s&'
                 'clientid=%s&psessionid=&t={rand}') %
            (self.ptwebqq, self.clientid),
            Referer=('http://s.web2.qq.com/proxy.html?v=20130916001'
                     '&callback=1&id=1'),
            Origin='http://s.web2.qq.com'
        )['vfwebqq']
        self.logger.info('已获取vfwebqq')

    def __get_UinAndPsessionid(self):
        result = self.qqsession.smartQQ_request(
            url='http://d1.web2.qq.com/channel/login2',
            data={
                'r': json.dumps({
                    'ptwebqq': self.ptwebqq, 'clientid': self.clientid,
                    'psessionid': '', 'status': 'online'
                })
            },
            Referer=('http://d1.web2.qq.com/proxy.html?v=20151105001'
                     '&callback=1&id=2'),
            Origin='http://d1.web2.qq.com'
        )
        self.uin = result['uin']
        self.psessionid = result['psessionid']
        self.hash = qHash(self.uin, self.ptwebqq)
        self.bkn = bknHash(self.qqsession.session.cookies['skey'])
        self.logger.info('已获取uin和psessionid')

    def __get_info(self):
        # 请求一下 get_online_buddies 页面，避免103错误。
        # 若请求无错误发生，则表明登录成功
        self.qqsession.smartQQ_request(
            url=('http://d1.web2.qq.com/channel/get_online_buddies2?'
                 'vfwebqq=%s&clientid=%d&psessionid=%s&t={rand}') %
            (self.vfwebqq, self.clientid, self.psessionid),
            Referer=('http://d1.web2.qq.com/proxy.html?v=20151105001&'
                     'callback=1&id=2'),
            Origin='http://d1.web2.qq.com'
        )

        self.logger.info('登录成功。登录账号：%s(%s)' % (self.nick, self.qq))
