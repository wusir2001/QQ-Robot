#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-30 09:34:07
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cndockysudo
# @Version : $Id$s


if __name__ == '__main__':
    from qqRobot import app
    import  time
    t = 1
    while t > 0:
        try:
            app.start()
        except:
            t -= 1
            time.sleep(180)
            continue
