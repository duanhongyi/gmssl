pysm4
========


### SM4算法

国密SM4(无线局域网SMS4)算法， 一个分组算法， 分组长度为128bit， 密钥长度为128bit，
算法具体内容参照[SM4算法](https://drive.google.com/file/d/0B0o25hRlUdXcbzdjT0hrYkkwUjg/view?usp=sharing)。

pysm4是国密SM4算法的Python实现， 提供了`encrypt`、 `decrypt`、 `encrypt_ecb`、 `decrypt_ecb`、 `encrypt_cbc`、
`decrypt_cbc`等函数用于加密解密， 用法如下：

#### 1. 初始化`CryptSM4`

```python
from pysm.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
from pysm.func import padding, unpadding, str_to_list, list_to_str

key = '3l5butlj26hvv313'
value = '111'
iv = [0] * 16
crypt_sm4 = CryptSM4()
```

#### 2. `encrypt_ecb`和`decrypt_ecb`

```python

crypt_sm4.set_key(str_to_list(key), SM4_ENCRYPT)
encrypt_value = crypt_sm4.crypt_ecb(padding(str_to_list(value)))
crypt_sm4.set_key(str_to_list(key), SM4_DECRYPT)
decrypt_value = unpadding(crypt_sm4.crypt_ecb(encrypt_value))
assert value == list_to_str(decrypt_value)
```

#### 3. `encrypt_cbc`和`decrypt_cbc`

```python

crypt_sm4.set_key(str_to_list(key), SM4_ENCRYPT)
encrypt_value = crypt_sm4.crypt_cbc(iv , padding(str_to_list(value)))
crypt_sm4.set_key(str_to_list(key), SM4_DECRYPT)
decrypt_value = unpadding(crypt_sm4.crypt_cbc(iv , encrypt_value))
assert value == list_to_str(decrypt_value)
```
