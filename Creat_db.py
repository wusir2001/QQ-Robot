#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-05 21:46:36
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : $Id$


from SmartQQ.models import engine, Base

if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
