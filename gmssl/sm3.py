#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : sm3.py
# @Author: yubo
# @Date  : 2019/12/16
# @Desc  :

from .libsm3 import lib_sm3, sm3_hash

if lib_sm3 is None:
    from .sm3_implement import *
    using_libsm3 = False
else:
    from .libsm3 import *
    using_libsm3 = True

#print(sm3_hash(b'01'))
assert sm3_hash(b'01').upper() == "7f4528abbaeb75420d8ae5842f12b221deb73722d49e02fccb461450e0c1d7ad".upper()