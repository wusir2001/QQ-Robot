#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-08 15:26:44
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://bitwater1997.cn
# @Version : $Id$


from .QQUser import QQUser
from .QQSession import QQSession
from .QQUtils import qHash
from .QQMessage import QQMessage
import requests
import logging
import json


class QQClient(object):
    """docstring for QQClient"""

    def __init__(self):
        self.clientid = 53999199
        self.qqsession = QQSession()
        self.qquser = QQUser(self.qqsession, self.clientid)
        self.logger = logging.getLogger('QQSDK.QQClient')

    def login(self):
        self.qquser.login()

    def logout(self):
        pass

    def clear(self):
        pass

    def get_message(self):
        self.logger.info('getting message')
        data = {'r': json.dumps({
            "ptwebqq": "\#{%s}" % (self.qquser.ptwebqq),
            "clientid": self.clientid,
            "psessionid": "\#{%s}" % (self.qquser.psessionid),
            "key": ""
        })}
        try:
            result = self.qqsession.smartQQ_request('http://d1.web2.qq.com/channel/poll2', data=data,
                                                    Referer='http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2', timeout=120)
        except requests.exceptions.ReadTimeout:
            self.logger.info('timeout')
        else:
            self.logger.info('Origin receive message:%s', str(result))
            if result is None:
                return None
            value = result[0]['value']

            content = ""
            for i in range(1, len(value['content'])):
                content = content + str(value['content'][i])

            qm = QQMessage(
                poll_type=result[0]['poll_type'],
                time=value['time'],
                msg_id=value['msg_id'],
                content=content,
                to_uin=value['to_uin'],
                from_uin=value['from_uin'],
                send_uin=value['send_uin'] if 'send_uin' in value else None,
                did=value['did'] if 'did' in value else None,
                group_code=value['group_code'] if 'group_code' in value else None
            )
            self.logger.info(str(qm))
            return qm

    def send_message_to_persion(self, message):
        self.__send_message("to",
                            url="http://d1.web2.qq.com/channel/send_buddy_msg2",
                            to_id=message.from_uin, text=message.reply)

    def send_message_to_group(self, message):
        self.__send_message("group_uin",
                            url="http://d1.web2.qq.com/channel/send_qun_msg2", to_id=message.group_code, text=message.reply)

    def send_message_to_discuss(self, message):
        self.__send_message("did",
                            url="http://d1.web2.qq.com/channel/send_discu_msg2",
                            to_id=message.did, text=message.reply)

    def __send_message(self, to, url, to_id, text):
        self.logger.info('Send message: %s\n', text)
        data = {'r': json.dumps({"%s" % (to): int(to_id),
                                 "content": "[\"%s\",[\"font\",{\"name\":\"宋体\",\"size\":10,\"style\":[0,0,0],\"color\":\"000000\"}]]" % (text),
                                 "face": 339,
                                 "clientid": 53999199,
                                 "msg_id": 89260007,
                                 "psessionid": "%s" % (self.qquser.psessionid)})}

        self.qqsession.smartQQ_request(url=url, data=data,
                                       Referer="http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2")

    def get_user_friends(self):
        self.logger.info('start to get_user_friends')
        url = 'http://s.web2.qq.com/api/get_user_friends2?'
        data = {'vfwebqq': self.qquser.vfwebqq,
                'hash': qHash(self.qquser.uin, self.qquser.ptwebqq)
                }
        result = self.qqsession.smartQQ_request(url=url, data=data, timeout=1000,
                                                Referer='http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1',
                                                Origin='http://s.web2.qq.com')
        self.logger.info('success to get_user_friends')
        return result['info'], result['marknames']

    def get_friend_info(self, uin):
        url = 'http://s.web2.qq.com/api/get_friend_info2?tuin=%s&vfwebqq=%s&clientid=%s&psessionid=%s&t={rand}' % (
            uin, self.qquser.vfwebqq, self.clientid, self.qquser.psessionid)
        result = self.qqsession.smartQQ_request(url=url, timeout=1000,
                                                Referer='http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1')
        return result

    def get_qq_nub_from_uin(self, uin):
        info = self.get_friend_info(uin)
        email = info['email'].split('@')
        return email[0]
