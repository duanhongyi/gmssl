from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
import random


def test_sm4_cbc(basic_loop, rand_bytes):
    for _ in range(basic_loop):
        crypt_sm4 = CryptSM4()
        msg = rand_bytes(random.randint(1,100))
        key = rand_bytes(16)
        iv = rand_bytes(16)

        crypt_sm4.set_key(key, SM4_ENCRYPT)
        enc = crypt_sm4.crypt_cbc(iv, msg)

        crypt_sm4.set_key(key, SM4_DECRYPT)
        dec = crypt_sm4.crypt_cbc(iv, enc)

        assert dec == msg


def test_sm4_ecb(basic_loop, rand_bytes):
    for _ in range(basic_loop):
        crypt_sm4 = CryptSM4()
        msg = rand_bytes(random.randint(1,100))
        key = rand_bytes(16)
        iv = rand_bytes(16)

        crypt_sm4.set_key(key, SM4_ENCRYPT)
        enc = crypt_sm4.crypt_ecb(msg)

        crypt_sm4.set_key(key, SM4_DECRYPT)
        dec = crypt_sm4.crypt_ecb(enc)

        assert dec == msg


if __name__ == '__main__':
    key = b'3l5butlj26hvv313'
    value = b'111'
    iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    crypt_sm4 = CryptSM4()

    crypt_sm4.set_key(key, SM4_ENCRYPT)
    encrypt_value = crypt_sm4.crypt_ecb(value)
    crypt_sm4.set_key(key, SM4_DECRYPT)
    decrypt_value = crypt_sm4.crypt_ecb(encrypt_value)
    assert value == decrypt_value

    crypt_sm4.set_key(key, SM4_ENCRYPT)
    encrypt_value = crypt_sm4.crypt_cbc(iv, value)
    crypt_sm4.set_key(key, SM4_DECRYPT)
    decrypt_value = crypt_sm4.crypt_cbc(iv, encrypt_value)
    assert value == decrypt_value