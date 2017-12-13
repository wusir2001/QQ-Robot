#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-05 22:56:06
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : $Id$

import time
import logging
from .models import DBsession, ChatMessage, Admin, Friend, Group, Discuss


class Bothistory(object):

    def __init__(self):
        self.logger = logging.getLogger('qqRobot.Bothistory')

    def clear(self):
        session = DBsession()
        session.query(Friend).delete()
        session.commit()
        session.close()

    """
        user_name = Column(String(20), index=True)
        user_qq = Column(Integer, nullable=False)
        message_type = Column(String(10), nullable=False)

        from_name = Column(String(20), index=True)
        from_qq = Column(Integer)

        from_text = Column(Text)
        reply_text = Column(Text)
    """

    def save_chat_message(self, user_name, user_qq, message_type, from_name, from_qq, from_text, reply_text):
        cm = ChatMessage(
            user_name=user_name,
            user_qq=user_qq,
            message_type=message_type,
            from_name=from_name,
            from_qq=from_qq,
            from_text=from_text,
            reply_text=reply_text
        )
        session = DBsession()
        session.add(cm)
        session.commit()
        session.close()

    '''
        user_qq = Column(String(20), primary_key=True)
        user_name = Column(String(20))
    '''

    def save_admin(self, user_qq, user_name):
        self.logger.info('save_admin')
        session = DBsession()
        ad = session.query(Admin).filter(Admin.user_qq == user_qq).first()
        if not ad:
            ad = Admin(user_qq=user_qq, user_name=user_name)
            session.add(ad)
        else:
            ad.timestamp = time.time()
        session.commit()
        session.close

    def save_friends(self, friends):
        self.logger.info('save_friends')
        session = DBsession()
        for f in friends:
            session.add(Friend(*f))
        session.commit()
        session.close()

    def save_groups(self, groups):
        self.logger.info('save_groups')
        session = DBsession()
        for g in groups:
            session.add(Group(*g))
        session.commit()
        session.close()

    def save_discuss(self, discuss):
        self.logger.info('save_discuss')
        session = DBsession()
        for d in discuss:
            session.add(Discuss(*d))
        session.commit()
        session.close()

    def get_user_info_from_uin(self, uin):
        self.logger.info("get_user_info_from_uin : %s", uin)
        session = DBsession()
        user = session.query(Friend).filter(Friend.uin == uin).first()
        return user
