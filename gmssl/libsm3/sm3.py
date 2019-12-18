#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : sm3.py.py
# @Author: yubo
# @Date  : 2019/12/16
# @Desc  :

import ctypes
from .libsm3 import *
from math import ceil
import binascii

def sm3_hash(in_msg):
    sm3_ctx = SM3Context()
    hash_buffer = (ctypes.c_ubyte * 32)()
    sm3_starts(ctypes.POINTER(SM3Context)(sm3_ctx))
    array_type = ctypes.c_ubyte * len(in_msg)
    sm3_update(ctypes.POINTER(SM3Context)(sm3_ctx), array_type(*in_msg), ctypes.c_int(len(in_msg)))
    sm3_finish(ctypes.POINTER(SM3Context)(sm3_ctx), hash_buffer)
    return bytes([i for i in hash_buffer]).hex()


def sm3_hmac(key, in_msg):
    pass

def sm3_kdf(z, klen):  # z为16进制表示的比特串（str），klen为密钥长度（单位byte）
    klen = int(klen)
    ct = 0x00000001
    rcnt = ceil(klen / 32)
    zin = [i for i in bytes.fromhex(z.decode('utf8'))]
    ha = ""
    for i in range(rcnt):
        msg = zin + [i for i in binascii.a2b_hex(('%08x' % ct).encode('utf8'))]
        ha = ha + sm3_hash(msg)
        ct += 1
    return ha[0: klen * 2]

class SM3:
    def __init__(self):
        self._sm3_ctx = SM3Context()

    def start(self, msg=None):
        sm3_starts(ctypes.POINTER(SM3Context)(self._sm3_ctx))
        self.update(msg)

    def update(self, msg):
        if msg is not None:
            array_type = ctypes.c_ubyte * len(msg)
            sm3_update(ctypes.POINTER(SM3Context)(self._sm3_ctx), array_type(*msg), ctypes.c_int(len(msg)))

    def finish(self, msg=None):
        self.update(msg)
        hash_buffer = (ctypes.c_ubyte * 32)()
        sm3_finish(ctypes.POINTER(SM3Context)(self._sm3_ctx), hash_buffer)
        return bytes([i for i in hash_buffer]).hex()


