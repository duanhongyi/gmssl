GMSSL
========
GmSSL是一个开源的加密包的python实现，支持SM2/SM3/SM4等国密(国家商用密码)算法、项目采用对商业应用友好的类BSD开源许可证，开源且可以用于闭源的商业应用。

### 安装

```shell
pip install gmssl
```

### SM2算法
RSA算法的危机在于其存在亚指数算法，对ECC算法而言一般没有亚指数攻击算法
SM2椭圆曲线公钥密码算法：我国自主知识产权的商用密码算法，是ECC（Elliptic Curve Cryptosystem）算法的一种，基于椭圆曲线离散对数问题，计算复杂度是指数级，求解难度较大，同等安全程度要求下，椭圆曲线密码较其他公钥算法所需密钥长度小很多。

gmssl是包含国密SM2算法的Python实现， 提供了 `encrypt`、 `decrypt`等函数用于加密解密， 用法如下：

#### 1. 初始化`CryptSM2`

```python
import base64
import binascii
from gmssl import sm2, func
#16进制的公钥和私钥
private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
sm2_crypt = sm2.CryptSM2(
    public_key=public_key, private_key=private_key)
```

#### 2. `encrypt`和`decrypt`

```python
#数据和加密后数据为bytes类型
data = b"111"
enc_data = sm2_crypt.encrypt(data)
dec_data =sm2_crypt.decrypt(enc_data)
assert dec_data == data
```

#### 3. `sign`和`verify`
```python
data = b"111" # bytes类型
random_hex_str = func.random_hex(sm2_crypt.para_len)
sign = sm2_crypt.sign(data, random_hex_str) #  16进制
assert sm2_crypt.verify(sign, data) #  16进制
```

#### 4. SM2withSM3签名的`sign`和`verify`

```python
data = b"111" # bytes类型
sign = sm2_crypt.sign_SM2withSM3(data) #  16进制
assert sm2_crypt.verify_SM2withSM3(sign, data) #  16进制
```

### SM4算法

国密SM4(无线局域网SMS4)算法， 一个分组算法， 分组长度为128bit， 密钥长度为128bit，
算法具体内容参照[SM4算法](https://drive.google.com/file/d/0B0o25hRlUdXcbzdjT0hrYkkwUjg/view?usp=sharing)。

gmssl是包含国密SM4算法的Python实现， 提供了 `encrypt_ecb`、 `decrypt_ecb`、 `encrypt_cbc`、
`decrypt_cbc`等函数用于加密解密， 用法如下：

#### 1. 初始化`CryptSM4`

```python
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT

key = b'3l5butlj26hvv313'
value = b'111' #  bytes类型
iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' #  bytes类型
crypt_sm4 = CryptSM4()
```

#### 2. `encrypt_ecb`和`decrypt_ecb`

```python

crypt_sm4.set_key(key, SM4_ENCRYPT)
encrypt_value = crypt_sm4.crypt_ecb(value) #  bytes类型
crypt_sm4.set_key(key, SM4_DECRYPT)
decrypt_value = crypt_sm4.crypt_ecb(encrypt_value) #  bytes类型
assert value == decrypt_value

```

#### 3. `encrypt_cbc`和`decrypt_cbc`

```python

crypt_sm4.set_key(key, SM4_ENCRYPT)
encrypt_value = crypt_sm4.crypt_cbc(iv , value) #  bytes类型
crypt_sm4.set_key(key, SM4_DECRYPT)
decrypt_value = crypt_sm4.crypt_cbc(iv , encrypt_value) #  bytes类型
assert value == decrypt_value

```
