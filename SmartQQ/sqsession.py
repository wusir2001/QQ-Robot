#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 17:27:08
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : 1.0


import io
import sys
import time
import requests
import random
from PIL import Image
import json
from . import logger


class SQSession(object):

    def __init__(self):
        self.session = requests.session()
        self.session.headers.update({
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9;'
                           ' rv:27.0) Gecko/20100101 Firefox/27.0'),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })
        self.clientid = 53999199

    def login(self):
        self._prepare_session()
        self._wait_auth()
        self._get_Ptwebqq()
        self._get_Vfwebqq()
        self._get_UinAndPsessionid()
        self._test_login()

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

        logger.info('登录成功。登录账号：%s(%s)' % (self.nick, self.qq))

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
        QR_code = io.BytesIO()
        QR_code.write(self._get_QRcode())
        img = Image.open(QR_code)
        img.show()

    def _wait_auth(self):
        self._show_QRcode()
        while True:
            time.sleep(3)
            authStatus = self._get_auth_status().decode('utf-8')
            if '二维码未失效' in authStatus:
                logger.info('等待二维码扫描及授权...')
            elif '二维码认证中' in authStatus:
                logger.info('二维码已扫描，等待授权...')
            elif '二维码已失效' in authStatus:
                logger.warning('二维码已失效, 重新获取二维码')
                self._show_QRcode()
            elif '登录成功' in authStatus:
                logger.info('已获授权')
                items = authStatus.split(',')
                self.nick = str(items[-1].split("'")[1])
                self.qq = str(int(self.session.cookies['superuin'][1:]))
                self.urlPtwebqq = items[2].strip().strip("'")
                break
            else:
                logger.error('获取二维码扫描状态时出错, html="%s"' % (authStatus))
                sys.exit(1)

    def _get_Ptwebqq(self):
        self._get_url(self.urlPtwebqq)
        self.ptwebqq = self.session.cookies['ptwebqq']
        logger.info('已获取ptwebqq')

    def _get_Vfwebqq(self):
        self.vfwebqq = self._smartQQ_request(
            url=('http://s.web2.qq.com/api/getvfwebqq?ptwebqq=%s&'
                 'clientid=%s&psessionid=&t={rand}') %
            (self.ptwebqq, self.clientid),
            Referer=('http://s.web2.qq.com/proxy.html?v=20130916001'
                     '&callback=1&id=1'),
            Origin='http://s.web2.qq.com'
        )['vfwebqq']
        logger.info('已获取vfwebqq')

    def _get_url(self, url, data=None, Referer=None, Origin=None):

        Referer and self.session.headers.update({'Referer': Referer})
        Origin and self.session.headers.update({'Origin': Origin})
        timeout = 30 if url != 'https://d1.web2.qq.com/channel/poll2' else 120

        if data is None:
            return self.session.get(url, timeout=timeout)
        else:
            return self.session.post(url, data=data, timeout=timeout)

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
        logger.info('已获取uin和psessionid')

    def _smartQQ_request(self, url, data=None, Referer=None, Origin=None,
                         expectedCodes=(0, 100003, 100100)):

        url = url.format(rand=repr(random.random()))
        resp = self._get_url(url, data, Referer, Origin)
        html = resp.content.decode('utf8')
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
            return result


def bknHash(skey, init_str=5381):
    hash_str = init_str
    for i in skey:
        hash_str += (hash_str << 5) + ord(i)
    hash_str = int(hash_str & 2147483647)
    return hash_str


def qHash(x, K):
    N = [0] * 4
    for T in range(len(K)):
        N[T % 4] ^= ord(K[T])

    U, V = 'ECOK', [0] * 4
    V[0] = ((x >> 24) & 255) ^ ord(U[0])
    V[1] = ((x >> 16) & 255) ^ ord(U[1])
    V[2] = ((x >> 8) & 255) ^ ord(U[2])
    V[3] = ((x >> 0) & 255) ^ ord(U[3])

    U1 = [0] * 8
    for T in range(8):
        U1[T] = N[T >> 1] if T % 2 == 0 else V[T >> 1]

    N1, V1 = '0123456789ABCDEF', ''
    for aU1 in U1:
        V1 += N1[((aU1 >> 4) & 15)]
        V1 += N1[((aU1 >> 0) & 15)]

    return V1


if __name__ == '__main__':
    qs = SQSession()
    qs.login()
    print(qs.ptwebqq)
    print(qs.vfwebqq)
    print(qs.psessionid)
    print(qs.clientid)
    print(qs.uin)
