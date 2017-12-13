#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-05 21:46:36
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : $Id$


from qqRobot.models import engine, Base


def creatdb():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    creatdb()
