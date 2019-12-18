#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : sm2_helper.py
# @Author: yubo
# @Date  : 2019/11/14
# @Desc  :

import math
from .sm2_parameter import *

class Point(object):
    def __init__(self,x=0,y=0):
        self._x=x
        self._y=y
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = value
    '''
    def distance(self,p1,p2):
        return((p1.x-p2.x)**2+(p1.y-p2.y)**2)**0.5
    def isnearby(self,p):
        return((self.x-p.x)**2+(self.y-p.y)**2)**0.5
    '''
    def __str__(self):
        return '('+str(self.x)+', '+str(self.y)+')'


def remove_0b_at_beginning(a):
    if (a[0:2] == '0b'):
        a = a[2:len(a)]
    return a


def padding_0_to_length(S, length):
    temp = S
    S = ''
    if (temp[0:2] == '0b'):
        S = S + '0b'
        temp = temp[2:len(temp)]
    for i in range(0, length - len(temp)):
        S = S + '0'
    for i in range(0, len(temp)):
        S = S + temp[i]
    return S


'''
input：非负整数x，以及字节串的目标长度k  
output：长度为k的字节串M
'''


def int_to_bytes(x, k):
    # print("--- 整数到字节串的转换 ---")
    # temp = x
    # i = k - 1
    M = []
    for i in range(0, k):
        M.append(x >> (i * 8) & 0xff)
    M.reverse()
    '''
    M = ''
    while (i >= 0):
        a = temp // (2**(8*i))
        M = M + str(a)
        temp = temp - a * (2**(8*i))
        i = i - 1
    '''
    return M


# '''
### test int_to_bytes ###
# print(int_to_bytes(1024,5))   #[0, 0, 0, 0, 255]
# '''

# 4.2.2 字节串到整数
'''
input：长度为k的字节串M
output：整数x
'''


def bytes_to_int(M):
    # print("--- 字节串到整数的转换 ---")
    # k = int(len(M))
    # i = 0
    x = 0
    for b in M:
        x = x * 256 + int(b)
    '''
    while (i < k):
        x = x + int( M[k-i-1:k-i] ) * (2**(8*i)) 
        i = i + 1
    '''
    return x


'''
### test bytes_to_int ###
print(bytes_to_int('0020'))   # 257
'''

# 4.2.3 比特串到字节串
'''
intput：长度为m的比特串s
output：长度为k的字节串M，其中k=m/8(上整)
'''


def bits_to_bytes(s):
    # print("--- 比特串到字节串的转换 ---")
    if s[0:2] == '0b':
        s = s.replace('0b', '')
        m = len(s)
        k = math.ceil(m / 8)
        M = []
        for i in range(0, k):
            temp = ''
            j = 0
            while j < 8:
                if (8 * i + j >= m):
                    # M.append(s >> 0 & 0xff)
                    temp = temp + '0'
                else:
                    # M.append(s >> (i*8) & 0xff)
                    temp = temp + s[m - (8 * i + j) - 1:m - (8 * i + j)]
                # print(i , "-", j, "-", m-(8*i+j)-1, "-", temp)
                j = j + 1
            temp = temp[::-1]
            temp = int(temp, 2)
            M.append(temp)
        # M = M + temp
        M.reverse()
    else:
        print("*** ERROR: 输入必须为比特串 *** function：bits_to_bytes(s) ***")
        return -1;
    return M


'''
### test bits_to_bytes ###
'''
# print(bits_to_bytes('0b100011111101'))

# '''

# 4.2.4 字节串到比特串
'''
input：长度为k的字节串M
output：长度为m的比特串s，其中m=8k
'''


def bytes_to_bits(M):
    # print("--- 字节串到比特串的转换 ---")
    k = len(M)
    m = 8 * k
    temp = ''
    s = 0
    M.reverse()
    j = 0
    for i in M:
        s = s + i * (256 ** j)
        j = j + 1
    s = bin(s)
    s = padding_0_to_length(s, m)
    M.reverse()
    return s


### test bytes_to_bits ###
# print(bytes_to_bits([2,2]))

# 4.2.5 域元素到字节串
'''
input：Fq中的元素a，模数q
output：长度l=t/8（取上整）的字节串S，其中t=lb(q)(取上整)
'''
def ele_to_bytes(a):
    # print("--- 域元素到字节串的转换 ---")
    S = []
    q = get_q()
    if (is_q_prime() and q % 2 == 1):  # q为奇素数
        if (a >= 0 and a <= q - 1):
            t = math.ceil(math.log(q, 2))
            l = math.ceil(t / 8)
            S = int_to_bytes(a, l)
        else:
            print("*** ERROR: 域元素须在区间[0, q-1]上 *** function：ele_to_bytes(a) ***")
            return -1;
    elif is_q_power_of_two():  # q为2的幂
        if type(a) == str and a[0:2] == '0b':
            m = math.ceil(math.log(q, 2))
            a = padding_0_to_length(a, m)
            '''temp = a
                                                a = ''
                                                for i in range(0, 2):
                                                    a = a + temp[i]
                                                for i in range(0, m-len(temp)+2):
                                                    a = a + '0'
                                                for i in range(0, len(temp)-2):
                                                    a = a + temp[i+2]'''
            if len(a) - 2 == m:
                S = bits_to_bytes(a)
            else:
                print("*** ERROR: 域元素必须为长度为m的比特串 *** function：ele_to_bytes(a)")
                return -1;
        else:
            print("*** ERROR: 输入必须为比特串 *** function：ele_to_bytes(a) ***")
            return -1;
    else:
        print("*** ERROR: q不满足奇素数或2的幂 *** function：ele_to_bytes(a) ***")
        return -1;
    return S


### test ele_to_bytes ###
# print(ele_to_bytes(256, 257))
# print(ele_to_bytes('0b101101010'))

# 4.2.6 字节串到域元素
'''
input：基域Fq的类型（模数q），长度为l=t/8（取上整）的字节串S，其中t=lb(q)(取上整)
output：Fq中的元素a
'''


def bytes_to_ele(q, S):
    a = ''
    if (is_q_prime() and q % 2 == 1):  # q为奇素数
        a = 0
        t = math.ceil(math.log(q, 2))
        l = math.ceil(t / 8)
        a = bytes_to_int(S)
        if not (a >= 0 and a <= q - 1):
            print("*** ERROR: 域元素须在区间[0, q-1]上 *** function：bytes_to_ele(q, S) ***")
            return -1;
    elif is_q_power_of_two():  # q为2的幂
        m = math.ceil(math.log(q, 2))
        a = padding_0_to_length(a, m)
        '''a = bytes_to_bits(S)
                                temp = a
                                a = ''
                                for i in range(0, 2):
                                    a = a + temp[i]
                                for i in range(0, m-len(temp)+2):
                                    a = a + '0'
                                for i in range(0, len(temp)-2):
                                    a = a + temp[i+2]'''
        if not len(a) - 2 == m:
            print("*** ERROR: 域元素必须为长度为m的比特串 *** function：bytes_to_ele(q, S)")
            return -1;
    else:
        print("*** ERROR: q不满足奇素数或2的幂 *** function：bytes_to_ele(q, S) ***")
        return -1;
    return a


### test bytes_to_ele(q, S) ###
# print(bytes_to_ele(257, '20'))
# print(bytes_to_ele(256, [232]))
# print(bytes_to_ele(1024, [1, 86]))

# 4.2.7 域元素到整数
'''
input：域Fq中的元素a，模数q
output：整数x
'''
'''
def ele_to_int(a):
	#print("--- 域元素到整数的转换 ---")
	x = 0
	 # q为奇素数
	x = a
	return x

def ele_to_int_2m(a):
	#print("--- 域元素到整数的转换 ---")
	x = 0
	q = config.config.get_q()()
	# q为2的幂
	if type(a)==str and a[0:2] == '0b':
		m = math.log(q, 2)
		if len(a)-2 == m:
			a = a.replace('0b', '')
			for i in a:
				x = x * 2 + int(i)
		else:
			print("*** ERROR: 域元素必须为长度为m的比特串 *** function：ele_to_int(a, q)")
			return -1;
	else:
		print("*** ERROR: 输入必须为比特串 *** function：ele_to_int(a, q) ***")
		return -1;
	return x
'''


def ele_to_int(a):
    # print("--- 域元素到字节串的转换 ---")
    x = 0
    q = get_q()
    if (is_q_prime() and q % 2 == 1):  # q为奇素数
        x = a
    elif is_q_power_of_two():  # q为2的幂
        if type(a) == str and a[0:2] == '0b':
            m = math.log(q, 2)
            if len(a) - 2 == m:
                # a = a.replace('0b', '')
                a = remove_0b_at_beginning(a)
                for i in a:
                    x = x * 2 + int(i)
            else:
                print("*** ERROR: 域元素必须为长度为m的比特串 *** function：ele_to_int(a, q)")
                return -1;
        else:
            print("*** ERROR: 输入必须为比特串 *** function：ele_to_int(a, q) ***")
            return -1;
    else:
        print("*** ERROR: q不满足奇素数或2的幂 *** function：ele_to_int(a, q) ***")
        return -1;
    return x


### test ele_to_int ###
# print(ele_to_int(256, 257))
# print(ele_to_int('0b1011', 16))

# 4.2.8 点到字符串
'''
input：椭圆曲线上的点P=(xp,yp)，且P!=Q
output：字节串S。
			若选用未压缩表示形式或混合表示形式，则输出字节串长度为2l+1；
			若选用压 缩表示形式，则输出字节串长度为l+1。
			（l=lb(q)/8(取上整)）
'''


def point_to_bytes(point):
    q = get_q()
    l = math.ceil(math.log(q, 2) / 8)
    x = point.x
    y = point.y
    S = []
    PC = ''
    # a. 将域元素x转换成长度为l的字节串X
    X = ele_to_bytes(x)
    temp = X
    X = []
    for i in range(0, l - len(temp)):
        X.append(0)
    for i in range(0, len(temp)):
        X.append(temp[i])
    '''
    ##### b. 压缩表示形式 #####
    # b.1 计算比特y1
    temp = ele_to_bytes(y)
    y1_temp = bytes_to_bits(temp)#[math.ceil(math.log(q,2)/8)*8-1:math.ceil(math.log(q,2)/8)*8]
    y1 = y1_temp[len(y1_temp)-1:len(y1_temp)]
    # b.2 若y1=0，则令PC=02；若y1=1，则令PC=03
    if y1 == '0':
        PC = 2
    elif y1 == '1':
        PC = 3
    else:
        print('ERROR')
    # b.3 字节串S=PC||X
    S.append(PC)
    for i in X:
        S.append(i)
    '''
    '''
    ##### c. 未压缩表示形式 #####
    # c.1 将域元素y转换成长度为l的字节串Y
    Y = ele_to_bytes(y)
    # c.2 令PC=04
    PC = 4
    # c.3 字节串S=PC||X||Y
    S.append(PC)
    for m in X:
        S.append(m)
    for n in Y:
        S.append(n)
    '''
    ##### d. 混合表示形式 #####
    # d.1 将域元素y转换成长度为l的字节串Y
    Y = ele_to_bytes(y)
    temp = Y
    Y = []
    for i in range(0, l - len(temp)):
        Y.append(0)
    for i in range(0, len(temp)):
        Y.append(temp[i])
    # d.2 计算比特y1
    y1_temp = bytes_to_bits(Y)  # [math.ceil(math.log(q,2)/8)*8-1:math.ceil(math.log(q,2)/8)*8]
    y1 = y1_temp[len(y1_temp) - 1:len(y1_temp)]
    # d.3 若y1=0，则令PC=06；若y1=1，则令PC=07
    if y1 == '0':
        PC = 6
    elif y1 == '1':
        PC = 7
    else:
        print('*** ERROR: PC值不对 function: point_to_bytes ***')
    # d.4 字节串S=PC||X||Y
    S.append(PC)
    for m in X:
        S.append(m)
    for n in Y:
        S.append(n)
    return S


### test point_to_bytes
# config.set_q(211)
# point = Point(142, 15)
# print(point_to_bytes(point))


# 4.2.9 字符串到点
'''
input：定义Fq上椭圆曲线的域元素a、b，字节串S
output：椭圆曲线上的点P=(xp,yp)，且P!=Q
'''


def bytes_to_point(a, b, S):
    q = get_q()
    l = math.ceil(math.log(q, 2) / 8)
    PC = ''
    X = []
    Y = []
    # a.
    if len(S) == 2 * l + 1:  # 为压缩表示形式或者混合表示形式
        PC = S[0]
        for i in range(1, l + 1):
            X.append(S[i])
        for i in range(l + 1, 2 * l + 1):
            Y.append(S[i])
    elif len(S) == l + 1:  # 压缩表示形式
        PC = S[0]
        for i in range(1, l):
            X.append(S[i])
    else:
        print('*** ERROR: wrong size  function: bytes_to_point ***')

    # b. 将X转换成与元素x
    x = bytes_to_ele(q, X)
    ##### c. 压缩表示形式 #####
    y1 = ''
    # c.1 and c.2
    if PC == 2:
        y1 = '0'
    elif PC == 3:
        y1 = '1'
    ##### d. 未压缩表示形式 #####
    elif PC == 4:
        y = bytes_to_ele(q, Y)
    ##### e. 混合表示形式 #####
    # e.1 and e.2
    elif PC == 6 or 7:
        y = bytes_to_ele(q, Y)
    else:
        print('ERROR in bytes_to_point')
    # f.
    result = 0
    if (type(x) != type(1)):
        x = int(x, 2)
    if (type(y) != type(1)):
        y = int(y, 2)
    if (is_q_prime() and q % 2 == 1):  # q为奇素数
        if (y ** 2) % q != (x ** 3 + a * x + b) % q:
            return -1
    elif is_q_power_of_two():
        if (y ** 2 + x * y) != (x ** 3 + a * x + b):
            return -1
    # g.
    point = Point(x, y)
    return point


# config.set_q(1024)
# print(bytes_to_point( 1, 0,[7, 0, 1, 0, 1]))

def bytes_to_str(S):
    temp = ''
    string = ''
    temp = remove_0b_at_beginning(bytes_to_bits(S))
    temp = padding_0_to_length(temp, 8 * math.ceil(len(temp) / 8))
    for i in range(0, math.ceil(len(temp) / 8)):
        string = string + chr(int(temp[i * 8:(i + 1) * 8], 2))
    return string


def str_to_bytes(x):
    S = []
    for i in x:
        S.append(ord(i))
    return S
##########################################################################################

# 多项式加法单位元 #
def polynomial_zero():
    return '0b0'


# 多项式乘法单位元 #
def polynomial_one():
    return '0b1'


# 多项式乘法 #
'''
input: 两个多项式（比特串）
output: 两个多项式的乘积
'''


def polynomial_times(a, b):
    # print("--- 多项式 乘法 ---")

    a_bytes = bits_to_bytes(a)
    a_int = bytes_to_int(a_bytes)
    b_bytes = bits_to_bytes(b)
    b_int = bytes_to_int(b_bytes)

    # max result length
    m = len(a) - 2 + len(b) - 2
    m_bytes = math.ceil(float(m) / 8.0)

    # counter
    i = 0
    # result
    c = 0
    while a_int != 0:
        if a_int % 2 == 1:
            c = c ^ (b_int << i)
        a_int = a_int // 2
        i += 1
    return bytes_to_bits(int_to_bytes(c, m_bytes))


### test polynomial_times ###
# print(polynomial_times('0b111', '0b11111001'))

# 多项式除法 #

'''
input: 被除多项式 a 和除多项式 b
output: a/b
'''


def polynomial_a_devide_b(a, b):
    # print("--- 多项式 除法 ---")

    a_bytes = bits_to_bytes(a)
    a_int = bytes_to_int(a_bytes)
    a_len = len(a_bytes)
    b_bytes = bits_to_bytes(b)
    b_int = bytes_to_int(b_bytes)
    b_len = len(b_bytes)

    # max result length
    m = len(a) - 2
    m_bytes = math.ceil(float(m) / 8.0)

    c = 0
    i = len(a) - len(b)
    while i >= 0:
        a_int = a_int ^ (b_int << i)
        c += (1 << i)
        i = len(bytes_to_bits(int_to_bytes(a_int, a_len))) \
            - len(bytes_to_bits(int_to_bytes(b_int, b_len)))
    return bytes_to_bits(int_to_bytes(c, m_bytes))


### test polynomial_a_devide_b ###
# print(polynomial_a_devide_b('0b1101101001110', '0b111011'))
# print(polynomial_a_devide_b('0b1011101110', '0b111'))

# 多项式取模 #
'''
input: 被除多项式 a 和除多项式 b
output: a/b 所余的多项式
'''


def polynomial_a_mod_b(a, b):
    # print("--- 多项式 取模 ---")

    a_bytes = bits_to_bytes(a)
    a_int = bytes_to_int(a_bytes)
    a_len = len(a_bytes)
    b_bytes = bits_to_bytes(b)
    b_int = bytes_to_int(b_bytes)
    b_len = len(b_bytes)

    # max result length
    m = len(b) - 1
    m_bytes = math.ceil(float(m) / 8.0)

    i = len(a) - len(b)
    while i >= 0:
        a_int = a_int ^ (b_int << i)
        i = len(bytes_to_bits(int_to_bytes(a_int, a_len))) \
            - len(bytes_to_bits(int_to_bytes(b_int, b_len)))

    return bytes_to_bits(int_to_bytes(a_int, m_bytes))
##########################################################################################

# 判断是否为有限域元素 #
def in_field(a):
    q = get_q()
    # q 为奇素数
    if is_q_prime() and q > 2:
        if not (a >= 0 and a<= q-1):
            print("*** ERROR: a不是有限域中元素 *** function: in_field ***")
            return False
        else:
            return True
    # q 为 2 的幂
    elif is_q_power_of_two():
        m = math.log2(q)
        if (len(a)-2) > m:
            print("*** ERROR: a 不是有限域元素 *** function: in_field ***")
            return False
        else:
            for i in range(2, len(a)):
                if a[i] != '0' and a[i] != '1':
                    print("*** ERROR: a 不是有限域元素 *** function: in_field ***")
                    return False
            return True
    else:
        print("*** ERROR: 模数q不是奇素数或者2的幂 *** function: field_ele_add ***")
        return -1


# 有限域加法单位元 #
def field_ele_zero():
    q = get_q()
    # q 为奇素数
    if is_q_prime() and q > 2:
        return 0
    # q 为 2 的幂
    elif is_q_power_of_two():
        m = int(math.log2(q))
        zero = '0b'
        for i in range(0, m):
            zero += '0'
        return zero
    else:
        print("*** ERROR: 模数q不是奇素数或者2的幂 *** function: field_ele_zero ***")
        return -1
### test field_ele_zero ###
#config.set_q(16)
#print(field_ele_zero())

# 有限域乘法单位元 #
def field_ele_one():
    q = get_q()
    # q 为奇素数
    if is_q_prime() and q > 2:
        return 1
    # q 为 2 的幂
    elif is_q_power_of_two():
        m = int(math.log2(q))
        one = '0b'
        for i in range(0, m - 1):
            one += '0'
        one += '1'
        return one
    else:
        print("*** ERROR: 模数q不是奇素数或者2的幂 *** function: field_ele_one ***")
        return -1
### test field_ele_one ###
#config.set_q(16)
#print(field_ele_one())

# 3.1 有限域计算 #
# 有限域加法 #
'''
input: 域元素 a 和 b
output: 域元素 (a+b)
'''
def field_ele_add(a, b):
    #print("--- 有限域 加法 ---")

    q = get_q()
    # q 为奇素数
    if is_q_prime() and q > 2:
        if not in_field(a):
            print("*** ERROR: a不是素域中元素 *** function: field_ele_add ***")
            return -1
        elif not in_field(b):
            print("*** ERROR: b不是素域中元素 *** function: field_ele_add ***")
            return -1
        else:
            return((a + b) % q)
    # q 为 2 的幂
    elif is_q_power_of_two():
        #m = math.log2(q)
        if not (in_field(a) and in_field(b)):
            print("*** ERROR: 参数不是二元扩域元素 *** function: field_ele_add ***")
            return -1
        else:
            c_int = ele_to_int(a) ^ (ele_to_int(b))
            c_bytes = int_to_bytes(c_int, 2)
            c_ele = bytes_to_ele(q, c_bytes)
            return c_ele
    else:
        print("*** ERROR: 模数q不是奇素数或者2的幂 *** function: field_ele_add ***")
        return -1
### test field_ele_add ###
#config.set_q(997)
#print(field_ele_add(996, 2))
#config.set_q(1024)
#print(field_ele_add('0b1010101010', '0b1111111100'))

# 有限域加法逆元 #
'''
input: 域元素 a
output: a 的逆元素
'''
def field_ele_inverse_add(a):
    q = get_q()
    # q 为奇素数
    if is_q_prime() and q > 2:
        if not in_field(a):
            print("*** ERROR: a不是域中元素 *** function: field_ele_inverse_add ***")
            return -1
        else:
            return (q - a) % q
    # q 为 2 的幂
    elif is_q_power_of_two():
        #m = math.log2(q)
        if not in_field(a):
            print("*** ERROR: 参数不是二元扩域元素 *** function: field_ele_inverse_add ***")
            return -1
        else:
            return a
    else:
        print("*** ERROR: 模数q不是奇素数或2的幂 *** function: field_ele_inverse_add ***")
        return -1
### test field_ele_inverse_add ###
#config.set_q(23)
#print(field_ele_inverse_add(8))
#config.set_q(16)
#config.set_fx('0b10011')
#print(field_ele_inverse_add('0b0101'))

# 有限域减法 #
'''
input: 被减元素 a 和减元素 b
output: 域元素 (a-b)
'''
def field_ele_sub(a, b):
    return field_ele_add(a, field_ele_inverse_add(b))

# 有限域乘法 #
'''
input: 域元素 a 和 b
output: 域元素 (a*b)
'''
def field_ele_times(a, b):
    #print("--- 有限域 乘法 ---")

    q = get_q()
    # q 为奇素数
    if is_q_prime() and q > 2:
        if not in_field(a):
            print("*** ERROR: a不是域中元素 *** function: field_ele_times ***")
            return -1
        elif not in_field(b):
            print("*** ERROR: b不是域中元素 *** function: field_ele_times ***")
            return -1
        else:
            return((a * b) % q)
    # q 为 2 的幂
    elif is_q_power_of_two():
        #m = math.log2(q)
        if not (in_field(a) and in_field(b)):
            print("*** ERROR: 参数不是二元扩域元素 *** function: field_ele_times ***")
            return -1
        else:
            result_bits = polynomial_a_mod_b(polynomial_times(a, b), config.get_fx())
            return bytes_to_ele(q, bits_to_bytes(result_bits))
    else:
        print("*** ERROR: 模数q不是奇素数或2的幂 *** function: field_ele_times ***")
        return -1
### test field_ele_time ###
#config.set_q(997)
#print(field_ele_times(56, 46))
#config.set_q(16)
#config.set_fx('0b10011')
#print(field_ele_times('0b0100', '0b1110'))

# 有限域幂运算 #
'''
iuput: 域元素 g 和 幂次 a
output: 域元素 g**a
'''
def field_ele_g_pow_a(g, a):
    #print("--- 有限域 幂运算 ---")

    q = get_q()
    # q 为奇素数
    if is_q_prime() and q > 2:
        if not in_field(g):
            print("*** ERROR: a不是域中元素 *** function: field_ele_g_pow_a ***")
            return -1
        else:
            e = a % (q - 1)
            if e == 0:
                return 1
            r = int(math.log2(e))# + 1 - 1
            x = g
            for i in range(0, r):
                x = field_ele_times(x, x)
                if (e & (1 << (r - 1 - i))) == (1 << (r - 1 - i)):
                    x = field_ele_times(x, g)
            return x
    # q 为 2 的幂
    elif is_q_power_of_two():
        #m = math.log2(q)
        if not in_field(g):
            print("*** ERROR: 参数不是二元扩域元素 *** function: field_ele_g_pow_a ***")
            return -1
        else:
            e = a % (q -1)
            if e == 0:
                return polynomial_one()
            r = int(math.log2(e))# + 1 - 1
            x = g
            for i in range(0, r):
                x = field_ele_times(x, x)
                if (e & (1 << (r - 1 - i))) == (1 << (r - 1 - i)):
                    x = field_ele_times(x, g)
            return x
    else:
        print("*** ERROR: 模数q不是奇素数或2的幂 *** function: field_ele_g_pow_a ***")
        return -1
### test field_ele_g_pow_a ###
#config.set_q(23)
#print(field_ele_g_pow_a(8, 2))
#config.set_q(16)
#config.set_fx('0b10011')
#print(field_ele_g_pow_a('0b0010', 9))

# 有限域逆元素 #
'''
input: 元素 a
output: 元素 a 的逆元素
'''
def field_ele_inverse_times(a):
    q = get_q()
    # q 为奇素数
    if is_q_prime() and q > 2:
        if not in_field(a):
            print("*** ERROR: a不是域中元素 *** function: field_ele_inverse_times ***")
            return -1
        else:
            return field_ele_g_pow_a(a, get_q() - 2)
    # q 为 2 的幂
    elif is_q_power_of_two():
        #m = math.log2(q)
        if not in_field(a):
            print("*** ERROR: 参数不是二元扩域元素 *** function: field_ele_inverse_times ***")
            return -1
        else:
            return field_ele_g_pow_a(a, get_q() - 2)
    else:
        print("*** ERROR: 模数q不是奇素数或2的幂 *** function: field_ele_inverse_times ***")
        return -1
### test field_ele_inverse_times ###
#config.set_q(23)
#print(field_ele_inverse_times(8))
#config.set_q(16)
#config.set_fx('0b10011')
#print(field_ele_inverse_times('0b0010'))

# 有限域除法 #
'''
input: 被除数 a 和除数 b
output: 除法所得商
'''
def field_ele_a_devide_b(a, b):
    #print("--- 有限域 除法 ---")
    return field_ele_times(a, field_ele_inverse_times(b))
### test field_ele_a_devide_b ###
#config.set_q(23)
#print(field_ele_a_devide_b(3, 8))
#config.set_q(16)
#config.set_fx('0b10011')
#print(field_ele_a_devide_b('0b1001', '0b0101'))

# 3.2.3 椭圆曲线群 #

# 椭圆曲线无穷远点 #
def ECG_ele_zero():
    return Point(field_ele_zero(), field_ele_zero())

# 椭圆曲线元素判断 #
# 元素为零 #
def ECG_ele_is_zero(p):
    if p.x == field_ele_zero() and p.y == field_ele_zero():
        return True
    else:
        return False
# 元素互为逆元素 #
def ECG_is_inverse_ele(p1, p2):
    q = get_q()
    # q 为素数
    if is_q_prime():
        if p1.x == p2.x and p1.y == field_ele_inverse_add(p2.y):
            return True
        else:
            return False
    elif is_q_power_of_two():
        if p1.x == p2.x and p2.y == field_ele_add(p1.x, p1.y):
            return True
        else:
            return False
    else:
        print("*** ERROR: q 不是素数或者 2 的幂 *** function: ECG_is_inverse_ele ***")
        return False
# 元素相等 #
def ECG_ele_equal(p1, p2):
    if p1.x == p2.x and p1.y == p2.y:
        return True
    else:
        return False

# 椭圆曲线加法 #
'''
input: 椭圆曲线群中点 a 和 b
output: 椭圆曲线群中点(a+b)
'''
def ECG_ele_add(p1, p2):
    # Fp 上的椭圆曲线群
    if is_q_prime():
        if ECG_ele_is_zero(p1):
            return p2
        elif ECG_ele_is_zero(p2):
            return p1
        elif ECG_is_inverse_ele(p1, p2):
            return ECG_ele_zero()
        elif ECG_ele_equal(p1, p2):
            #lam = (3 * (p1.x**2) + config.get_a()) / (2 * p1.y)
            t1 = field_ele_add(field_ele_times(3, field_ele_g_pow_a(p1.x, 2)), get_a())
            t2 = field_ele_times(2, p1.y)
            lam = field_ele_a_devide_b(t1, t2)
            #x = lam**2 - 2 * p1.x
            x = field_ele_sub(field_ele_g_pow_a(lam, 2), field_ele_times(2, p1.x))
            #y = lam * (p1.x - x) - p1.y
            y = field_ele_sub(field_ele_times(lam, field_ele_sub(p1.x, x)), p1.y)
            return Point(x, y)
        else:
            #lam = (p2.y - p1.y) / (p2.x - p1.x)
            lam = field_ele_a_devide_b(field_ele_sub(p2.y, p1.y), field_ele_sub(p2.x, p1.x))
            #x = lam * lam - p1.x - p2.x
            x = field_ele_sub(field_ele_sub(field_ele_g_pow_a(lam, 2), p1.x), p2.x)
            #y = lam * (p1.x - x) - p1.y
            y = field_ele_sub(field_ele_times(lam, field_ele_sub(p1.x, x)), p1.y)
            return Point(x, y)

    # F2^m 上的椭圆曲线
    if is_q_power_of_two():
        if ECG_ele_is_zero(p1):
            return p2
        elif ECG_ele_is_zero(p2):
            return p1
        elif ECG_is_inverse_ele(p1, p2):
            return ECG_ele_zero()
        elif ECG_ele_equal(p1, p2):
            #lam = p1.x + (p1.y / p1.x)
            lam = field_ele_add(p1.x, field_ele_a_devide_b(p1.y, p1.x))
            #x = lam**2 + lam + config.get_a()
            x = field_ele_add(field_ele_add(field_ele_g_pow_a(lam, 2), lam), get_a())
            #y = p1.x**2 + (lam + 1) * x
            y = field_ele_add(field_ele_g_pow_a(p1.x, 2), \
                field_ele_times(field_ele_add(lam, field_ele_one()), x))
            return Point(x, y)
        else:
            #lam = (p1.y + p2.y) / (p1.x + p2.x)
            lam = field_ele_a_devide_b(field_ele_add(p1.y, p2.y), \
                field_ele_add(p1.x, p2.x))
            #x = lam**2 + lam + p1.x + p2.x + config.get_a()
            t1 = field_ele_add(field_ele_g_pow_a(lam, 2), lam)
            t2 = field_ele_add(field_ele_add(p1.x, p2.x), get_a())
            x = field_ele_add(t1, t2)
            #y = lam * (p1.x + x) + x + p1.y
            t1 = field_ele_times(lam, field_ele_add(p1.x, x))
            t2 = field_ele_add(x, p1.y)
            y = field_ele_add(t1, t2)
            return Point(x, y)

# 椭圆曲线求 2 倍点 #
'''
input: 椭圆曲线点 p
output: 点(P+P)
'''
def ECG_double_point(p):
    # Fp 上的椭圆曲线群
    if is_q_prime():
        if ECG_ele_is_zero(p):
            return p
        else:
            t1 = field_ele_add(field_ele_times(3, field_ele_g_pow_a(p.x, 2)), get_a())
            t2 = field_ele_times(2, p.y)
            lam = field_ele_a_devide_b(t1, t2)
            x = field_ele_sub(field_ele_g_pow_a(lam, 2), field_ele_times(2, p.x))
            y = field_ele_sub(field_ele_times(lam, field_ele_sub(p.x, x)), p.y)
            return Point(x, y)
    # F2^m 上的椭圆曲线
    if is_q_power_of_two():
        if ECG_ele_is_zero(p):
            return p
        else:
            lam = field_ele_add(p.x, field_ele_a_devide_b(p.y, p.x))
            x = field_ele_add(field_ele_add(field_ele_g_pow_a(lam, 2), lam), get_a())
            y = field_ele_add(field_ele_g_pow_a(p.x, 2), \
                field_ele_times(field_ele_add(lam, field_ele_one()), x))
            return Point(x, y)


# 椭圆曲线求 k 倍点 #
'''
input: 倍数 k 和椭圆曲线点 p
output: p 的 k 倍点
'''
def ECG_k_point(k, p):
    #print('[' + str(k) + ']P')
    l = int(math.log2(k)) + 1# - 1
    #print(l)
    point_q = ECG_ele_zero()
    for i in range(0, l):
        #print('i = ' + str(i))
        j = l - 1 - i
        #t_start = time.time()
        point_q = ECG_double_point(point_q)
        #t_end = time.time()
        #print('double:' + str(t_end - t_start))
        if (k & (1 << j)) == (1 << j):
            #t_start = time.time()
            point_q = ECG_ele_add(point_q, p)
            #t_end = time.time()
            #print('add:' + str(t_end - t_start))
    return point_q

# Fp 椭圆曲线测试 #
#config.set_q(23)
#config.set_a(1)
#config.set_b(1)
### test ECG_ele_add ###
#print(ECG_ele_add(Point(3, 10), Point(9, 7)))   #(3, 10) + (9, 7) = (17, 20)
### test ECG_double_point ###
#print(ECG_double_point(Point(3, 10)))   # 2(3, 10) = (7, 12)
### test ECG_k_point ###
#print(ECG_k_point(3, Point(3, 10)))

# F2^m 椭圆曲线测试 #
#config.set_q(32)
#config.set_fx('0b100101')
#config.set_a('0b00001')
#config.set_b('0b00001')
### test ECG_ele_add ###
# (01010, 11000) + (01000, 11111) = (11110, 10101)
#print(ECG_ele_add(Point('0b01010', '0b11000'), Point('0b01000', '0b11111')))
### test ECG_double_point ###
# [2](01010, 11000) = (01000, 11111)
#print(ECG_double_point(Point('0b01010', '0b11000')))
### test ECG_k_point ###
# [3](01010, 11000) = (11110, 10101)
#print(ECG_k_point(3, Point('0b01010', '0b11000')))

# 6.1 密钥对的生成 #
'''
input: 有效的椭圆曲线系统参数集合
output: 与输入参数相关的一个密钥对(d, P)
'''
def key_pair_generation():
    '''
    config.set_q(parameters['q'])
    config.set_a(parameters['a'])
    config.set_b(parameters['b'])
    n = parameters['n']
    point_g = Point(parameters['Gx'], parameters['Gy'])
    # q 为 2 的幂
    if config.is_q_power_of_two():
        config.set_fx(parameters['f(x)'])
    '''
    point_g = Point(get_Gx(), get_Gy())
    n = get_n()

    d = random.randint(1, n - 2)
    p = ECG_k_point(d, point_g)
    keypair = []
    keypair.append(d)
    keypair.append(p)
    return keypair


def fix_integer(num):
    int_hex = hex(num)[2:]
    return '0'*(64-len(int_hex)) + int_hex


# 产生密钥对 #
def sm2_key_pair_gen():
    key_pair = key_pair_generation()
    prive_key = key_pair[0]
    pub_key = bytes_to_str(point_to_bytes(key_pair[1]))

    #print("~私钥")
    #print(hex(prive_key))

    #print("!公钥")
    a = get_a()
    b = get_b()
    point = (bytes_to_point(a, b, str_to_bytes(pub_key)))
    #print(hex(point.x), hex(point.y))

    return fix_integer(prive_key), fix_integer(point.x)+fix_integer(point.y)
