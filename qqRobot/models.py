#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-09 06:33:05
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : 1.0

import time
from .bitconfig import Datebase_path
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Integer, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base


# 初始化数据库连接:
engine = create_engine(Datebase_path)
metadata = MetaData(engine)

Base = declarative_base()


timestamp_size = 30
name_size = 50
uin_size = 20
qq_size = 20


'''
    聊天记录,该表永久保存
'''


class ChatMessage(Base):
    __tablename__ = "ChatMessage"
    id = Column(Integer, primary_key=True)
    timestamp = Column(String(timestamp_size),
                       nullable=False, default=str(time.time()))

    message_type = Column(String(10), nullable=False)
    from_text = Column(Text)
    reply_text = Column(Text)

    # group_uin = Column(String(uin_size))
    # did_uin = Column(String(uin_size))

    user_qq = Column(String(qq_size), nullable=False)
    user_name = Column(String(qq_size))

    from_qq = Column(String(qq_size), nullable=False)
    from_name = Column(String(qq_size))

    def __repr__(self):
        return "<User(user:%s(%s),type:%s,from:%s(%s),text(from):%s,text(reply):%s )>" % (
            self.user_name, self.user_qq,
            self.message_type,
            self.from_name, self.from_qq, self.from_text, self.reply_text)


class Admin(Base):
    __tablename__ = "admin"
    user_qq = Column(String(qq_size), primary_key=True)
    user_name = Column(String(name_size))
    timestamp = Column(String(timestamp_size),
                       nullable=False, default=str(time.time()))

    def __init__(self, user_qq, user_name):
        self.user_name = user_name
        self.user_qq = user_qq
        self.timestamp = str(time.time())

    def __repr__(self):
        return "<Admin( %s(%s) ) > " % (self.user_qq, self.user_name)


# class Category(Base):
#     """docstring for Category"""
#     __tablename__ = "category"

#     index = Column(Integer, primary_key=True)
#     sort = Column(Integer)
#     name = Column(String(100))

#     def __repr__(self):
#         return "<Category( index:%s , sort:%s , name:%s )>" % (
#             self.index, self.sort, self.name)


class Friend(Base):
    __tablename__ = "friend"
    uin = Column(String(uin_size), primary_key=True)
    timestamp = Column(String(timestamp_size),
                       nullable=False, default=str(time.time()))

    user_qq = Column(String(qq_size))
    user_name = Column(String(name_size))
    mark_name = Column(String(name_size))  # 备注姓名

    # category_index = Column(Integer, ForeignKey('category.index'))
    def __init__(self, uin, user_name, mark_name, user_qq):
        self.uin = uin
        self.user_qq = user_qq
        self.user_name = user_name
        self.mark_name = mark_name

    def __repr__(self):
        return "<Friend( %s(%s) )" % (self.mark_name, self.user_qq)


DBsession = sessionmaker(bind=engine)
