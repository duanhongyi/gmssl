#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : pysm3.py
# @Author: yubo
# @Date  : 2019/12/12
# @Desc  :
import os, sys
import platform
import ctypes
import time
from functools import wraps

def timethis(func):
    '''
    Decorator that reports the execution time.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper

c_ubyte_p = ctypes.POINTER(ctypes.c_ubyte)


class SM3Context(ctypes.Structure):
    _fields_ = [("total", ctypes.c_ulong * 2),
                ("state", ctypes.c_ulong * 8),
                ("buffer", ctypes.c_ubyte * 64),
                ("ipad", ctypes.c_ubyte * 64),
                ("opad", ctypes.c_ubyte * 64)]


try:
    if platform.system() == "Windows":
        library_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "libsm3.dll")
    else:
        library_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "libsm3.so")
    lib_sm3 = ctypes.CDLL(library_path)
except Exception as e:
    lib_sm3 = None

if lib_sm3 is not None:
    sm3_starts = lib_sm3.sm3_starts
    sm3_starts.restype = None
    sm3_starts.argtypes = (ctypes.POINTER(SM3Context), )

    sm3_update = lib_sm3.sm3_update
    sm3_update.restype = None
    sm3_update.argtypes = (ctypes.POINTER(SM3Context), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int)

    sm3_finish = lib_sm3.sm3_finish
    sm3_finish.restype = None
    sm3_finish.argtypes = (ctypes.POINTER(SM3Context), ctypes.POINTER(ctypes.c_ubyte * 32))

    libsm_sm3 = lib_sm3.sm3
    libsm_sm3.restype = None
    libsm_sm3.argtypes = (ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte * 32))


data = bytes.fromhex("3031")
array_type = ctypes.c_ubyte * len(data)
hash_buffer = (ctypes.c_ubyte * 32) ()
sm3 = libsm_sm3(array_type(*data), ctypes.c_int(len(data)), hash_buffer)
#print(hash_buffer.raw)

print("------")

sm3_ctx = SM3Context()
sm3_starts(ctypes.POINTER(SM3Context)(sm3_ctx))
sm3_update(ctypes.POINTER(SM3Context)(sm3_ctx), array_type(*data), ctypes.c_int(len(data)))
sm3_finish(ctypes.POINTER(SM3Context)(sm3_ctx), hash_buffer)
for i in hash_buffer:
    print(hex(i), end=" ")

@timethis
def test_sm3():
    with open("test.bin", 'rb') as f_in:
        sm3_ctx = SM3Context()
        sm3_starts(ctypes.POINTER(SM3Context)(sm3_ctx))
        data_read = f_in.read()
        print(len(data_read))
        array_type = ctypes.c_ubyte * len(data_read)
        sm3_update(ctypes.POINTER(SM3Context)(sm3_ctx), array_type(*data_read), ctypes.c_int(len(data_read)))
        sm3_finish(ctypes.POINTER(SM3Context)(sm3_ctx), hash_buffer)
        print("------")
        for i in hash_buffer:
            print(hex(i), end=" ")


for i in range(10):
    test_sm3()