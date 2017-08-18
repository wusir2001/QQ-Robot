#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 17:27:08
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : 1.0


import sys
import time
import requests
import random

import json
from .QMlog import Info, Warning, Error
from .QMutils import qHash, bknHash
from .QMQRcode import QMQRcode
from .QMdialmessage import QMdialmessage


class QMsession(object):

    def __init__(self):
        self.session = requests.session()
        self.session.headers.update({
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9;'
                           ' rv:27.0) Gecko/20100101 Firefox/27.0'),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })
        self.clientid = 53999199
        self.msgId = 6000000
        self._prepare_session()
        self.qmqrcode = QMQRcode()

    def login(self):
        self._wait_auth()
        self._get_Ptwebqq()
        self._get_Vfwebqq()
        self._get_UinAndPsessionid()
        self._test_login()

    def get_message(self):
        data = {'r': json.dumps({
            "ptwebqq": "\#{%s}" % (self.ptwebqq),
            "clientid": self.clientid,
            "psessionid": "\#{%s}" % (self.psessionid),
            "key": ""
        })}
        try:
            resp = self._get_url('http://d1.web2.qq.com/channel/poll2', data=data,
                                 Referer='http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2')
        except requests.exceptions.ReadTimeout:
            Info('timeout')
        else:
            message = resp.json()
            poll_type = message['result'][0]['poll_type']
            value = message['result'][0]['value']
            message_len = len(value['content'])
            content = ""
            for i in range(1, message_len):
                content = content + str(value['content'][i])
            if poll_type == 'message':
                return QMdialmessage(message_type=QMdialmessage.PERSION_MESSAGE,
                                     content=content,
                                     to_uin=value['to_uin'],
                                     from_uin=value['from_uin'],
                                     msg_id=value['msg_id'],
                                     time=value['time'],
                                     # msg_tpye=value['msg_type']
                                     )

            elif poll_type == 'group_message':
                return QMdialmessage(message_type=QMdialmessage.GROUP_MESSAGE,
                                     content=content,
                                     to_uin=value['to_uin'],
                                     group_code=value['group_code'],
                                     from_uin=value['from_uin'],
                                     send_uin=value['send_uin'],
                                     msg_id=value['msg_id'],
                                     time=value['time'],
                                     # msg_tpye=value['msg_type']
                                     )
            elif poll_type == 'discu_message':
                return QMdialmessage(message_type=QMdialmessage.DISCUSS_MESSAGE,
                                     content=content,
                                     to_uin=value['to_uin'],
                                     did=value['did'],
                                     send_uin=value['send_uin'],
                                     from_uin=value['from_uin'],
                                     msg_id=value['msg_id'],
                                     time=value['time'],
                                     # msg_tpye=value['msg_type']
                                     )
        return None

    def send_message_to_persion(self, message):
        # Info(message.reply)
        self._send_message("to", to_id=message.from_uin, text=message.reply)

    def send_message_to_group(self, message):
        # self._send_message(
            # "group_uin", to_id=message.group_uin, text=message.reply)
        pass

    def send_message_to_discuss(self, message):
        # self._send_message("did", to_id=message.did, text=message.reply)
        pass

    def _send_message(self, to, to_id, text):
        Info(text)
        data = {'r': json.dumps({"%s" % (to): int(to_id),
                                 "content": "[\"%s\",[\"font\",{\"name\":\"宋体\",\"size\":10,\"style\":[0,0,0],\"color\":\"000000\"}]]" % (text),
                                 "face": 339,
                                 "clientid": 53999199,
                                 "msg_id": 89260007,
                                 "psessionid": "%s" % (self.psessionid)})}
        # Info(data)

        r = self._smartQQ_request(url='https://d1.web2.qq.com/channel/send_buddy_msg2', data=data,
                                  Referer="http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2")

        # Info(self.session.headers)
        # Info(self.session.cookies)
        Info(r)

    def _test_login(self):
        # 请求一下 get_online_buddies 页面，避免103错误。
        # 若请求无错误发生，则表明登录成功
        self._smartQQ_request(
            url=('http://d1.web2.qq.com/channel/get_online_buddies2?'
                 'vfwebqq=%s&clientid=%d&psessionid=%s&t={rand}') %
            (self.vfwebqq, self.clientid, self.psessionid),
            Referer=('http://d1.web2.qq.com/proxy.html?v=20151105001&'
                     'callback=1&id=2'),
            Origin='http://d1.web2.qq.com'
        )

        Info('登录成功。登录账号：%s(%s)' % (self.nick, self.qq))

    def _get_auth_status(self):

        result = self._get_url(
            url='https://ssl.ptlogin2.qq.com/ptqrlogin?ptqrtoken=' +
                str(bknHash(self.session.cookies['qrsig'], init_str=0)) +
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

    def _prepare_session(self):
        self._get_url(
            'https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&'
            'style=16&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&'
            'no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&'
            'f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001')

        self.session.cookies.update({
            'RK': 'OfeLBai4FB',
            'pgv_pvi': '911366144',
            'pgv_info': 'ssid pgv_pvid=1051433466',
            'ptcz': ('ad3bf14f9da2738e09e498bfeb93dd9da7'
                     '540dea2b7a71acfb97ed4d3da4e277'),
            'qrsig': ('hJ9GvNx*oIvLjP5I5dQ19KPa3zwxNI'
                      '62eALLO*g2JLbKPYsZIRsnbJIxNe74NzQQ')
        })
        self._get_auth_status()
        self.session.cookies.pop('qrsig')

    def _get_QRcode(self):
        qrcode = self._get_url(
            'https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=0&l=M&' +
            's=5&d=72&v=4&t=' + repr(random.random())
        ).content
        return qrcode

    def _show_QRcode(self):
        self.qmqrcode.show_picture(self._get_QRcode())

    def _wait_auth(self):
        self._show_QRcode()
        while True:
            time.sleep(3)
            authStatus = self._get_auth_status().decode('utf-8')
            if '二维码未失效' in authStatus:
                Info('等待二维码扫描及授权...')
            elif '二维码认证中' in authStatus:
                Info('二维码已扫描，等待授权...')
            elif '二维码已失效' in authStatus:
                Warning('二维码已失效, 重新获取二维码')
                self._show_QRcode()
            elif '登录成功' in authStatus:
                Info('已获授权')
                items = authStatus.split(',')
                self.nick = str(items[-1].split("'")[1])
                self.qq = str(int(self.session.cookies['superuin'][1:]))
                self.urlPtwebqq = items[2].strip().strip("'")
                break
            else:
                Error('获取二维码扫描状态时出错, html="%s"' % (authStatus))
                sys.exit(1)

    def _get_Ptwebqq(self):
        self._get_url(self.urlPtwebqq)
        self.ptwebqq = self.session.cookies['ptwebqq']
        Info('已获取ptwebqq')

    def _get_Vfwebqq(self):
        self.vfwebqq = self._smartQQ_request(
            url=('http://s.web2.qq.com/api/getvfwebqq?ptwebqq=%s&'
                 'clientid=%s&psessionid=&t={rand}') %
            (self.ptwebqq, self.clientid),
            Referer=('http://s.web2.qq.com/proxy.html?v=20130916001'
                     '&callback=1&id=1'),
            Origin='http://s.web2.qq.com'
        )['vfwebqq']
        Info('已获取vfwebqq')

    def _get_UinAndPsessionid(self):
        result = self._smartQQ_request(
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
        self.bkn = bknHash(self.session.cookies['skey'])
        Info('已获取uin和psessionid')

    def _get_url(self, url, data=None, Referer=None, Origin=None):

        Referer and self.session.headers.update({'Referer': Referer})
        Origin and self.session.headers.update({'Origin': Origin})
        timeout = 30 if url != 'https://d1.web2.qq.com/channel/poll2' else 120

        if data is None:
            return self.session.get(url, timeout=timeout)
        else:
            return self.session.post(url, data=data, timeout=timeout)

    def _smartQQ_request(self, url, data=None, Referer=None, Origin=None,
                         expectedCodes=(0, 100003, 100100)):

        url = url.format(rand=repr(random.random()))
        html = self._get_url(url, data, Referer, Origin).content.decode('utf8')

        rst = json.loads(html)

        result = rst.get('result', rst)

        if 'retcode' in rst:
            retcode = rst['retcode']
        elif 'errCode' in rst:
            retcode = rst['errCode']
        elif 'ec' in rst:
            retcode = rst['ec']
        else:
            retcode = -1

        if (retcode in expectedCodes):
            Info('smartQQ request successful ! \n for result (%s)', result)
            return result
        else:
            Error('smartQQ_request has error ! \n for message (%s)', html)


if __name__ == '__main__':
    qs = SQSession()
    qs.login()
    print(qs.ptwebqq)
    print(qs.vfwebqq)
    print(qs.psessionid)
    print(qs.clientid)
    print(qs.uin)
