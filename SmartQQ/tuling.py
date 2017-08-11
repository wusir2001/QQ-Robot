#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-29 16:49:52
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : 1.0
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

import requests
# import json


class TulingSDK(object):
    """docstring for Tuling"""

    def __init__(self, APIkey, secret=None, userid='123456', api_url='http://www.tuling123.com/openapi/api'):
        self.APIkey = APIkey
        self.secret = secret
        self.api_url = api_url
        self.session = requests.session()
        self.userid = userid
        self.normal_code = [100000, 200000, 302000, 308000, 313000, 314000]

    def talk(self, info, loc=None):
        '''
           {
               “key”: “APIKEY”,
               “info”: “今天天气怎么样”,
               “loc”:“北京市中关村”,
               “userid”:“123456”
           }
        '''
        data = {}
        data['key'] = self.APIkey
        data['info'] = info
        data['userid'] = self.userid

        r = self.session.post(self.api_url, data=data)
        r.encoding = 'utf-8'

        '''
            In python 2.7 the defult code is ascii ,
            so if you want to transform the mes_dic.text to string.
            You will see the the next line.
            UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-3: ordinal not in range(128)
            so the first method is that you can use python3.x
            the second method is that you can reload the defult code as follow.
                import sys
                reload(sys)
                sys.setdefaultencoding('utf8')
            the final method is that you can use `str(mes_dic.text.encode('utf-8'))`
        '''

        return JsonDict(r.json())


class JsonDict(dict):
    ' general json object that allows attributes to be bound to and also behaves like a dict '

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(
                r"'JsonDict' object has no attribute '%s'" % attr)

    @property
    def content(self):
        ret = self['text'] + '\n'
        code = self['code']
        '''
        100000 文本类
        200000 链接类
        302000 新闻类
        308000 菜谱类
        313000(儿童版) 儿歌类
        314000(儿童版) 诗词类
        '''
        if code == 100000:
            return ret
        if code == 200000:
            return (ret + self['url'] + '\n')

        if code == 302000:
                # "article": "工信部:今年将大幅提网速降手机流量费",
                # "source": "网易新闻",
                # "icon": "",
                # "detailurl":
            for news in self['list']:

                ret = ret + '%s\n来源: %s\n图片: %s\n详情链接: %s\n' % (
                    news['article'], news['source'], news['icon'], news['detailurl'])
            return ret

        if code == 308000:
                # "name": "鱼香肉丝",
                # "icon":"http://i4.xiachufang.com/image/280/cb1cb7c49ee011e38844b8ca3aeed2d7.jpg",
                # "info": "猪肉、鱼香肉丝调料 | 香菇、木耳、红萝卜、黄酒、玉米淀粉、盐",
                # "detailurl": "http://m.xiachufang.com/recipe/264781/"
            for food in self['list']:

                ret = ret + '菜名: %s\n图片: %s\n菜谱信息: %s\n详情链接: %s\n' % (
                    food['name'], food['icon'], food['info'], food['detailurl'])
            return ret

        if code == 313000:
            # "function": {
            # "song": "刘德华",
            # "singer": "忘情水"
            # }

            return ret + '歌曲名:%s\n歌手: %s\n' % (self['function']['song'],
                                               self['function']['singer'])

        if code == 314000:
            # "text": "开始朗读诗词。",
            # "function": {
            # "author": "李白",
            # "name": "望庐山瀑布"
            # }

            return ret + '%s\n作者: %s\n' % (self['function']['name'],
                                           self['function']['author'])

        return ret
        # raise SDKError(code, ret)

    def __setattr__(self, attr, value):
        self[attr] = value


class SDKError(BaseException):
    """this error is from Tuling sdk"""

    def __init__(self, code, text):
        self.code = code
        self.text = text

    def __str__(self):
        return 'code : %s\ntext: %s\n' % (self.code, self.text)
