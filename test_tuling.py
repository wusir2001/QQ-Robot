#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-30 09:19:09
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : $Id$

from tuling import TulingSDK
import config


class test_main(object):
    """docstring for test_main"""

    def __init__(self, APIkey):
        # self.APIkey = APIkey
        self.tuling = TulingSDK(APIkey)

    def start(self):
        self._message_text()
        self._message_link()
        self._message_cook()
        self._message_train()
        self._message_childsong()
        self._message_poem()
        self._message_news()

    def repl_test(self):
        while True:
            info = raw_input()
            if info == 'exit':
                break
            resp = self.tuling.talk(info=info)
            print (resp)

    def _message_text(self):
        print (u"文字类")
        '''
            {
            “key”:“APIKEY”,
            “info”:“你好”
            }
        '''
        print (self.tuling.talk(info=u"你好"))

    def _message_link(self):
        print (u"链接类")
        '''
            {
            “key”: “APIKEY”,
            “info”: “小狗的图片”
            }
        '''
        print (self.tuling.talk(info=u"小狗的图片"))

    def _message_news(self):
        print (u"新闻类")
        '''
            {
            “key”: “APIKEY”,
            “info”: “我想看新闻”
            }
        '''
        print (self.tuling.talk(info=u"我想看新闻"))

    def _message_train(self):
        print (u"列车类")
        '''
            {
            “key”: “APIKEY”,
            “info”: “北京到拉萨的火车”
            }
        '''
        print (self.tuling.talk(info=u"北京到拉萨的火车"))

    def _message_cook(self):
        print (u"菜谱类")
        '''
            {
            “key”: “APIKEY”,
            “info”: “鱼香肉丝怎么做”
            }
        '''
        print (self.tuling.talk(info=u"鱼香肉丝怎么做"))

    def _message_childsong(self):
        print (u"儿歌类")
        '''
            {
            “key”: “APIKEY”,
            “info”: “给我唱一首刘德华的忘情水” ,
            14北京光年无限科技有限公司
            “userid”:“自定义唯一 userid(1-32 位,字母与数字组成)”
            }
        '''
        print (self.tuling.talk(info=u"给我唱一首刘德华的忘情水"))

    def _message_poem(self):
        print (u"诗词类")
        '''
            {
            “key”: “APIKEY”,
            “info”: “背一首李白的望庐山瀑布” ,
            “userid”:“自定义唯一 userid(1-32 位,字母与数字组成)”
            }
        '''
        print (self.tuling.talk(info=u"背一首李白的望庐山瀑布"))


if __name__ == '__main__':

    tm = test_main(APIkey=config.APIkey)
    # tm.start()
    tm.repl_test()
