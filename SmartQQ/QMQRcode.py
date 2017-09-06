#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-13 20:03:27
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : 1.0

# from PIL import Image
# import io
import codecs
from .QMlog import Info, Error
from .QMconfig import QRcode_path


class QMQRcode(object):

    def __init__(self, qrcode=None, ):
        self.qrcode = qrcode

    def show(self, qrcode=None):
        if qrcode:
            self.qrcode = qrcode
        if not self.qrcode:
            Error("there is no QRcode")
            return

        # # show the qrcode
        # QR_code = io.BytesIO()
        # QR_code.write(self.qrcode)
        # img = Image.open(QR_code)
        # img.show()
        # QR_code.close()
        Info("QRCODE_PATH : %s", QRcode_path)
        # save the qrcode
        with codecs.open(QRcode_path, 'wb') as f:
            f.write(self.qrcode)
        Info('success to save QRcode to %s', QRcode_path)
