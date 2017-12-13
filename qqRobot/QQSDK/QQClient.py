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

    def __init__(self, qr_path):
        self.clientid = 53999199
        self.qqsession = QQSession()
        self.qquser = QQUser(self.qqsession, self.clientid, qr_path)
        self.logger = logging.getLogger('QQSDK.QQClient')

    def login(self):
        self.logger.info('start login')
        self.qquser.login()
        self.logger.info('end login')

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
        except requests.exceptions.ConnectTimeout:
            self.logger.info('timeout')
        else:

            if result:
                value = result[0]['value']

                content = ""
                for i in range(1, len(value['content'])):
                    content = content + str(value['content'][i])

                return QQMessage(
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
            else:
                return None

    def send_message_to_persion(self, text, uin):
        self.logger.info('SendMsg2pers(%s):%s', uin, text)
        self.__send_message("to",
                            url="http://d1.web2.qq.com/channel/send_buddy_msg2",
                            to_id=uin, text=text)

    def send_message_to_group(self, text, group_code):
        self.logger.info('SendMsg2group(%s):%s', group_code, text)
        self.__send_message("group_uin",
                            url="http://d1.web2.qq.com/channel/send_qun_msg2", to_id=group_code, text=text)

    def send_message_to_discuss(self, text, did):
        self.logger.info('SendMsg2disc(%s):%s', did, text)
        self.__send_message("did",
                            url="http://d1.web2.qq.com/channel/send_discu_msg2",
                            to_id=did, text=text)

    def __send_message(self, to, url, to_id, text):
        data = {'r': json.dumps({"%s" % (to): int(to_id),
                                 "content": "[\"%s\",[\"font\",{\"name\":\"宋体\",\"size\":10,\"style\":[0,0,0],\"color\":\"000000\"}]]" % (text),
                                 "face": 339,
                                 "clientid": 53999199,
                                 "msg_id": 89260007,
                                 "psessionid": "%s" % (self.qquser.psessionid)})}

        self.qqsession.smartQQ_request(url=url, data=data,
                                       Referer="http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2")

    def get_friend_list(self):
        self.logger.info('start to get_user_friends')
        url = 'http://s.web2.qq.com/api/get_user_friends2?'
        data = {'vfwebqq': self.qquser.vfwebqq,
                'hash': qHash(self.qquser.uin, self.qquser.ptwebqq)}

        result = self.qqsession.smartQQ_request(url=url, data=data, timeout=1000,
                                                Referer='http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1',
                                                Origin='http://s.web2.qq.com')
        self.logger.info('success to get_user_friends')
        friends = []

        info = result['info']
        marknames = result['marknames']

        for i in info:
            tmp = [i['uin'], i['nick'], '', '']
            for mk in marknames:
                if i['uin'] == mk['uin']:
                    tmp[2] = mk['markname']
                    break
            tmp[3] = self.get_qq_nub_from_uin(i['uin'])
            friends.append(tmp)
        return friends

    def get_friend_info(self, uin):
        url = ('http://s.web2.qq.com/api/get_friend_info2?'
               'tuin=%s&vfwebqq=%s&clientid=%s&psessionid=%s&t={rand}' % (
                   uin, self.qquser.vfwebqq, self.clientid, self.qquser.psessionid))
        result = self.qqsession.smartQQ_request(url=url, timeout=1000,
                                                Referer='http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1')
        return result

    def get_group_list(self):
        self.logger.info('start to get_group_list')
        url = 'http://s.web2.qq.com/api/get_group_name_list_mask2'
        data = {'vfwebqq': self.qquser.vfwebqq,
                'hash': qHash(self.qquser.uin, self.qquser.ptwebqq)}
        result = self.qqsession.smartQQ_request(url=url, data=data, timeout=1000,
                                                Referer='http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1',
                                                Origin='http://s.web2.qq.com')
        self.logger.info('success to get_group_list')
        groups = []
        gnamelist = result['gnamelist']
        for gname in gnamelist:
            groups.append([gname['gid'], gname['name'], gname['code']])
        return groups

    def get_group_info(self, group_code):
        url = ('http://s.web2.qq.com/api/get_group_info_ext2?'
               'gcode=%s&vfwebqq=%s&t={rand}' % (
                   group_code, self.qquser.vfwebqq))
        result = self.qqsession.smartQQ_request(url=url, timeout=1000,
                                                Referer='http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1')
        return result

    def get_discus_list(self):
        self.logger.info('start get_discus_list ')
        url = ('http://s.web2.qq.com/api/get_discus_list?'
               'clientid=%s&psessionid=%s&vfwebqq=%s&t={rand}' % (
                   self.clientid, self.qquser.psessionid, self.qquser.vfwebqq))
        result = self.qqsession.smartQQ_request(url=url, timeout=1000,
                                                Referer='http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1')
        dnamelist = result['dnamelist']
        discuss = []
        for dname in dnamelist:
            discuss.append([dname['did'], dname['name']])
        return discuss

    def get_discus_info(self, did):
        url = ('http://d1.web2.qq.com/channel/get_discu_info?'
               'did=%s&vfwebqq=%s&clientid=%s&psessionid=%s&t={rand}' % (
                   did, self.qquser.vfwebqq, self.clientid, self.qquser.psessionid))
        result = self.qqsession.smartQQ_request(url=url, timeout=1000,
                                                Referer='http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1')
        return result

    def get_qq_nub_from_uin(self, uin):
        info = self.get_friend_info(uin)
        qqNub = info['email'].split('@')
        if qqNub:
            if qqNub[0] == 'www':
                if len(qqNub) >= 2:
                    return qqNub[1]
                else:
                    return None
            else:
                return qqNub[0]
        return None

    def get_self_info(self):
        url = 'http://s.web2.qq.com/api/get_self_info2&t=0.1'
        result = self.qqsession.smartQQ_request(url=url, timeout=1000,
                                                Referer='http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1')
        return result
