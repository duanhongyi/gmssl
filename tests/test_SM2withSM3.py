from gmssl import sm2

# 测试 SM2withSM3 签名算法
# 示例数据来自 GMT 0003.5-2012 A.2

if __name__ == '__main__':
    private_key = "3945208F7B2144B13F36E38AC6D39F95889393692860B51A42FB81EF4DF7C5B8"
    public_key = "09F9DF311E5421A150DD7D161E4BC5C672179FAD1833FC076BB08FF356F35020"\
                 "CCEA490CE26775A52DC6EA718CC1AA600AED05FBF35E084A6632F6072DA9AD13"
    random_hex_str = "59276E27D506861A16680F3AD9C02DCCEF3CC1FA3CDBE4CE6D54B80DEAC1BC21"

    sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
    data = b"message digest"

    print("-----------------test SM2withSM3 sign and verify---------------")
    sign = sm2_crypt.sign_SM2withSM3(data, random_hex_str)
    print('sign: %s' % sign)
    verify = sm2_crypt.verify_SM2withSM3(sign, data)
    print('verify: %s' % verify)
    assert verify
