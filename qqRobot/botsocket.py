#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-05 12:08:29
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : $Id$

import socket
import codecs
import _thread
import io
import logging

CLRF = b'\r\n'


class Botsocket(object):

    def __init__(self, QRcode_path, port=8888):
        self.QRcode_path = QRcode_path
        self.host = ""
        self.port = port
        self.logger = logging.getLogger('qqRobot.Botsocket')

    def _creat_socket(self):

        # Configure socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        # passively wait, 3: maximum number of connections in the queue
        s.listen(3)

        self.logger.info("Sucess to creat socket server")

        while True:

            # accept and establish connection
            conn, addr = s.accept()

            # receive message
            request = conn.recv(1024)
            self.logger.debug('request is: %s,Connected by %s', request, addr)
            # send message
            bt = io.BytesIO()
            try:
                bt.write(b'HTTP/1.1 200 OK' + CLRF)
                with codecs.open(self.QRcode_path, "rb") as f:
                    cont = f.read()
                # size = len(cont)
                bt.write(b'Server: Apache/2.4.18 (Ubuntu)' + CLRF)
                bt.write(b'Content-Type: image/jpeg' + CLRF * 2)
                bt.write(cont)
            except OSError:
                bt.write(b'HTTP/1.1 400 Bad Request' + CLRF)
                bt.write(b'Content-Type: text/html' + CLRF * 2)
                bt.write(b'<h1>Not find the QRcode</h1>')
            self.logger.debug(bt.getvalue())
            conn.sendall(bt.getvalue())
            bt.close()
            conn.close()

    def start(self):
        _thread.start_new_thread(self._creat_socket, ())
