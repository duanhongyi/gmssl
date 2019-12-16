#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : sm3.py.py
# @Author: yubo
# @Date  : 2019/12/16
# @Desc  :

import ctypes
from .libsm3 import *


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