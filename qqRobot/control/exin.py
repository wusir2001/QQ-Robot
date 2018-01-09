#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 18-1-9
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://bitwater1997.cn
# @Version : 1.0

class Exin(object):
    '''
    独家开发的恶搞系统
    针对个人进行 持续轰炸
    '''
    def __init__(self,):
        self.__exlist = {}

    def isMatch(self,uin):
        if uin not in self.__exlist:
            return  None
        return  self.__exlist[uin]

    def set(self , uin , content = '你说什么,爸爸听不见'):
        self.__exlist[uin] = content


