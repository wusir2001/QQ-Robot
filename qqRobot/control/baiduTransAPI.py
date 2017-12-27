#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 17-12-27
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://bitwater1997.cn
# @Version : 1.0
import math
import random

# from .config import  baiduTran_APIID ,baiduTran_SECRET
import  hashlib
import  requests

class TransAPI(object):
    '''
        api doc http://api.fanyi.baidu.com/api/trans/product/apidoc
    '''

    def __init__(self,appid,secret):
        self.url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        self.appid = int(appid)
        self.secret = str(secret)


    def tran(self,text,_to='zh',_from='auto'):
        if len(text) > 200:
            raise BaiduAPIErr( 'the text length is to large')
        text = str(text)
        salt =  int(random.random() )
        # appid + q + salt + 密钥
        sign = str(self.appid)+text+str(salt)+self.secret

        sign = sign.encode('utf8')
        sign = hashlib.md5(sign).hexdigest()
        parames = {
            'q' :text,
            'from' :str(_from),
            'to':str(_to),
            'appid':self.appid,
            'salt':salt,
            'sign':sign
        }

        r = requests.get(url=self.url,params=parames).json()
        try:
            return  r['trans_result'][0]['dst']
        except :
            raise BaiduAPIErr(r)



class BaiduAPIErr(BaseException):

    def __init__(self,err):
        self.err= err

    def __str__(self):
        return  self.err

if __name__ == "__main__":
    api = TransAPI(baiduTran_APIID,baiduTran_SECRET)
    ret = api.tran(text='i love you ',_to='zh')
    print( ret )