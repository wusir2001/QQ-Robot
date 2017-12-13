#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-08 16:14:00
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://bitwater1997.cn
# @Version : $Id$

from .QQError import QQError
import logging
import requests
import json


class QQSession(object):
    """docstring for QQSession"""

    def __init__(self):
        self.logger = logging.getLogger('QQSDK.QQSession')
        self.session = requests.Session()
        self.logger.debug('初始化qqSession')
        self.__prepare_session()

    def __prepare_session(self):
        self.session.headers.update({
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9;'
                           ' rv:27.0) Gecko/20100101 Firefox/27.0'),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })
        self.get_url(
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

    def get_url(self, url, data=None, Referer=None, Origin=None, timeout=30):
        self.logger.debug('get_url:%s', url)
        Referer and self.session.headers.update({'Referer': Referer})
        Origin and self.session.headers.update({'Origin': Origin})

        if data is None:
            return self.session.get(url, timeout=timeout)
        else:
            return self.session.post(url, data=data, timeout=timeout)

    def smartQQ_request(self, url, data=None, Referer=None, Origin=None, timeout=None,
                        expectedCodes=(0, 100003, 100100)):
        self.logger.debug('smartQQ_rq: %s', url)
        url = url.format(rand='0.1')

        api_err_cnt = 0
        while True:

            html = self.get_url(url, data, Referer,
                                Origin).content.decode('utf8')

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
            else:
                self.logger.error(
                    'code(%s)smartQQ_request err! url:%s', retcode, url)
                if api_err_cnt < 5:
                    api_err_cnt += 1
                    continue

                raise QQError(
                    retcode, 'smartQQ_request err! url:%s' % (url))
