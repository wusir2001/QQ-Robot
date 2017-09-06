#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-06 17:14:04
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://www.bitwater1997.cn
# @Version : $Id$

import os
import sys
import time

# 产生子进程，而后父进程退出
pid = os.fork()
if pid > 0:
    sys.exit(0)

# 修改子进程工作目录
os.chdir("/")
# 创建新的会话，子进程成为会话的首进程
os.setsid()
# 修改工作目录的umask
os.umask(0)

# 创建孙子进程，而后子进程退出
pid = os.fork()
if pid > 0:
    sys.exit(0)

# 重定向标准输入流、标准输出流、标准错误
sys.stdout.flush()
sys.stderr.flush()
si = open("/dev/null", 'r')
so = open("/dev/null", 'a+')
se = open("/dev/null", 'a+', 0)
os.dup2(si.fileno(), sys.stdin.fileno())
os.dup2(so.fileno(), sys.stdout.fileno())
os.dup2(se.fileno(), sys.stderr.fileno())


from SmartQQ import QMcore
from config import APIkey
qm = QMcore(APIkey)
qm.start()
