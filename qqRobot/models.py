#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-09 06:33:05
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : 1.0

import time
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Integer, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# datebase
Datebase_path = 'sqlite:///' + \
    os.path.join(basedir, 'database/app.db')

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

    qq_nub = Column(String(qq_size), nullable=True)
    qq_name = Column(String(qq_size), nullable=True)
    group_name = Column(String(name_size), nullable=True)
    did_name = Column(String(name_size), nullable=True)

    self_qq = Column(String(qq_size))

    def __repr__(self):
        if self.group_name:
            return "<(%s)GroupMSG(%s)( %s:%s ) reply: %s" % (
                self.self_qq, self.group_name, self.qq_name,
                self.from_text, self.reply_text)
        elif self.did_name:
            return"<(%s)DiscuMSG(%s)( %s:%s ) reply: %s" % (
                self.self_qq, self.did_name, self.qq_name,
                self.from_text, self.reply_text)
        else:
            return "<(%s)MSG( %s:%s ) reply: %s" % (
                self.self_qq, self.qq_name,
                self.from_text, self.reply_text)


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


class Group(Base):
    __tablename__ = "group"
    gid = Column(String(uin_size), primary_key=True)
    name = Column(String(name_size))
    code = Column(String(uin_size))

    def __init__(self, gid, name, code):
        self.gid = gid
        self.name = name
        self.code = code

    def __repr__(self):
        return "<Group(gid:%s,name:%s,code:%s)>" % (self.gid, self.name, self.code)


class Discuss(Base):
    __tablename__ = "discuss"
    did = Column(String(uin_size), primary_key=True)
    name = Column(String(name_size))

    def __init__(self, did, name):
        self.did = did
        self.name = name

    def __repr(self):
        return "<Discuss(did:%s,name:%s)>" % (self.did, self.name)


DBsession = sessionmaker(bind=engine)
