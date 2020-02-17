#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : conftest.py
# @Author: yubo
# @Date  : 2019/12/18
# @Desc  :

import os
import pytest
import sys
import random

os.chdir(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir))

if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())
else:
    sys.path.insert(0, sys.path.pop(sys.path.index(os.getcwd())))

if os.path.join(os.getcwd(), 'tests') not in sys.path:
    sys.path.insert(1, os.path.join(os.getcwd(), 'tests'))


@pytest.fixture
def loop(request):
    return int(request.config.getoption("--loop"))


@pytest.fixture(scope='session')
def basic_loop():
    return 8

@pytest.fixture(scope='module')
def rand_bytes():
    def _rand_bytes(len):
        return bytes([random.randint(0, 255) for _ in range(len)])
    return _rand_bytes