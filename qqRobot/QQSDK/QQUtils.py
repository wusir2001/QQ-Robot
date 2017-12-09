#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-08 16:18:02
# @Author  : bitwater (bitwater1997@gmail.com)
# @Link    : http://bitwater1997.cn
# @Version : $Id$


def bknHash(skey, init_str=5381):
    hash_str = init_str
    for i in skey:
        hash_str += (hash_str << 5) + ord(i)
    hash_str = int(hash_str & 2147483647)
    return hash_str


def qHash(x, K):
    N = [0] * 4
    for T in range(len(K)):
        N[T % 4] ^= ord(K[T])

    U, V = 'ECOK', [0] * 4
    V[0] = ((x >> 24) & 255) ^ ord(U[0])
    V[1] = ((x >> 16) & 255) ^ ord(U[1])
    V[2] = ((x >> 8) & 255) ^ ord(U[2])
    V[3] = ((x >> 0) & 255) ^ ord(U[3])

    U1 = [0] * 8
    for T in range(8):
        U1[T] = N[T >> 1] if T % 2 == 0 else V[T >> 1]

    N1, V1 = '0123456789ABCDEF', ''
    for aU1 in U1:
        V1 += N1[((aU1 >> 4) & 15)]
        V1 += N1[((aU1 >> 0) & 15)]

    return V1
