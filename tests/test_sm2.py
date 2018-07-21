import base64
import binascii
from gmssl import sm2, func


if __name__ == '__main__':
    private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'

    sm2_crypt = sm2.CryptSM2(
        public_key=public_key, private_key=private_key)
    data = "111"
    enc_data = sm2_crypt.encrypt(data)
    print("enc_data:%s" % enc_data)
    print("enc_data_base64:%s" % base64.b64encode(bytes.fromhex(enc_data)))
    enc_data = '277FBCC5FC5271546ED1CB6BE38CE4FF071FCD3BDA71C31294819E74C2DCF1B5DDDB5BEC608B383967A7FC312A1DF17F3ABE52D5878B769148D7503AD315425C076FE26841DBC8F2C83AA1526C73527F93B4960FBE5D494ED608B301973543E087DAEF'
    dec_data = sm2_crypt.decrypt(enc_data)
    print("dec_data:%s" % bytes.fromhex(dec_data))

    print("-----------------test sign and verify---------------")
    random_hex_str = func.random_hex(sm2_crypt.para_len)
    sign = sm2_crypt.sign(data, random_hex_str)
    print('sign:%s' % sign)
    verify = sm2_crypt.verify(sign, data)
    print('verify:%s' % verify)
