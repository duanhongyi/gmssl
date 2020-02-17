import base64
import binascii
from gmssl import sm2, func
import random

private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'


def test_sm2_gen_key(basic_loop, rand_bytes):
    for _ in range(basic_loop):
        msg = rand_bytes(random.randint(1, 64))
        prikey, pubkey = sm2.sm2_key_pair_gen()

        crypto_sm2 = sm2.CryptSM2(private_key=prikey, public_key=pubkey)

        msg_enc = crypto_sm2.encrypt(msg)
        msg_dec = crypto_sm2.decrypt(msg_enc)
        assert msg == msg_dec

def test_sm2_sign(basic_loop, rand_bytes):
    for _ in range(basic_loop):
        msg = rand_bytes(random.randint(1, 64))
        prikey, pubkey = sm2.sm2_key_pair_gen()
        crypto_sm2 = sm2.CryptSM2(private_key=prikey, public_key=pubkey)
        signed_data = crypto_sm2.sign(msg)
        assert True == crypto_sm2.verify(signed_data, msg)

def test_sm2_enc_dec(basic_loop, rand_bytes):
    for _ in range(basic_loop):
        msg = rand_bytes(random.randint(1, 64))
        crypto_sm2 = sm2.CryptSM2(private_key=private_key, public_key=public_key)

        msg_enc = crypto_sm2.encrypt(msg)
        msg_dec = crypto_sm2.decrypt(msg_enc)
        assert msg == msg_dec


if __name__ == '__main__':
    sm2_crypt = sm2.CryptSM2(
        public_key=public_key, private_key=private_key)
    data = b"111"
    enc_data = sm2_crypt.encrypt(data)
    #print("enc_data:%s" % enc_data)
    #print("enc_data_base64:%s" % base64.b64encode(bytes.fromhex(enc_data)))
    dec_data = sm2_crypt.decrypt(enc_data)
    print(b"dec_data:%s" % dec_data)
    assert data == dec_data

    print("-----------------test sign and verify---------------")
    #random_hex_str = func.random_hex(sm2_crypt.para_len)
    sign = sm2_crypt.sign(data)
    print('sign:%s' % sign)
    verify = sm2_crypt.verify(sign, data)
    print('verify:%s' % verify)
    assert verify



