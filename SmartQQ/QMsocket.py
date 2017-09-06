#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-05 12:08:29
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : $Id$

import socket
import codecs
from .QMlog import Info
import _thread


class QMsocket(object):

    def __init__(self, QRcode_path, port=8000):
        self.QRcode_path = QRcode_path
        self.host = ""
        self.port = port

    def _creat_socket(self):

        # Configure socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))

        # passively wait, 3: maximum number of connections in the queue
        s.listen(3)
        Info("Sucess to creat socket server")
        while True:

            # accept and establish connection
            conn, addr = s.accept()

            # receive message
            # request = conn.recv(1024)
            # Info('request is: %s,Connected by %s', request, addr)

            # send message
            try:
                with codecs.open(self.QRcode_path, "rb") as f:
                    reply = f.read()
            except OSError:
                reply = "Not find the QRcode".encode("utf-8")

            conn.sendall(reply)
            # close connection
            conn.close()

    def start(self):
        _thread.start_new_thread(self._creat_socket, ())
