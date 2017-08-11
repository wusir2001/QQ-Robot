#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-13 20:03:27
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : 1.0

from PIL import Image
import io
import os
import codecs
from .QMlog import Info, Error
from .QMconfig import QRcode_pic_path


class QMQRcode(object):

    def __init__(self, qrcode=None, pic_path=None):
        self.qrcode = qrcode
        self.pic_path = pic_path

    def show_picture(self, qrcode=None):
        if qrcode:
            self.qrcode = qrcode
        if not self.qrcode:
            Error("there is no QRcode")
            return
        QR_code = io.BytesIO()
        QR_code.write(self.qrcode)
        img = Image.open(QR_code)
        img.show()
        QR_code.close()

    def save_piture(self, qrcode=None):
        if qrcode:
            self.qrcode = qrcode
        if not self.qrcode:
            Error("there is no QRcode")
            return

        path = os.path.join(QRcode_pic_path, 'qrcode.jpg')
        with codecs.open(path, 'rb') as f:
            f.write(self.qrcode)
        Info('success to save QRcode to %s', path)
