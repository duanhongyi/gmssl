#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : sm2_integer.py
# @Author: yubo
# @Date  : 2019/11/14
# @Desc  :
import math
import random


# 快速模指数算法 #
'''
input: 底数 g , 指数 a 和模数 p
output: (g**a)mod p
'''
def fast_pow(g, a, p):
    e = int(a % (p - 1))
    if e == 0:
        return 1
    r = int(math.log2(e))  # + 1 - 1
    x = g
    for i in range(0, r):
        x = int((x ** 2) % p)
        if (e & (1 << (r - 1 - i))) == (1 << (r - 1 - i)):
            x = (g * x) % p
    return int(x)


### test fast_pow ###
# print(fast_pow(5, 12, 23))

# Miller-Rabin检测 #
'''
input: 大奇数 u 和大正整数 T
output: 若 u 通过测试则输出 True，否则输出 False
'''


def isPrime_MR(u, T):
    # 计算 v 和 w ，使得 u - 1 = w * 2^v
    v = 0
    w = u - 1
    while w % 2 == 0:
        v += 1
        w = w // 2
    for j in range(1, T + 1):
        nextj = False
        a = random.randint(2, u - 1)
        b = fast_pow(a, w, u)
        if b == 1 or b == u - 1:
            nextj = True
            continue
        for i in range(1, v):
            b = (b ** 2) % u
            if b == u - 1:
                nextj = True
                break
            if b == 1:
                return False
        if not nextj:
            return False
    return True


### test isPrime_MR ###
# print(isPrime_MR(0xBDB6F4FE3E8B1D9E0DA8C0D46F4C318CEFE4AFE3B6B8551F, 10))
# print(isPrime_MR(23, 10))
# print(isPrime_MR(17, 10))

# 判断是否为2的幂
def is_Power_of_two(n):
    if n > 0:
        if (n & (n - 1)) == 0:
            return True
    return False


# if is_Power_of_two(45):
#	print('true')

# 求逆元
def inverse(a, n):
    a_ = fast_pow(a, n - 2, n) % n
    return a_
### test inverse ###
# print(inverse(3,7))
