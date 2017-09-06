#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-05 22:56:06
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : $Id$

import time
from .QMlog import Info, Warning, Error
from .models import DBsession, ChatMessage, Admin, Friend, engine


class QMhistory(object):

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

        session = DBsession()
        for f in friends:
            fri = Friend(*f)
            session.add(fri)
        session.commit()
        session.close()

    def get_user_info(self, uin):
        session = DBsession()
        user = session.query(Friend).filter(Friend.uin == uin).first()
        return user
