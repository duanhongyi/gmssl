
import random

for i in range(1):
    if i:
        from gmssl.libsm3 import sm3
    else:
        from gmssl import sm3_implement as sm3

    def test_sm3():
        y = sm3.sm3_hash(b"abc")
        assert y.upper() == "66C7F0F462EEEDD9D1F2D46BDC10E4E24167C4875CF2F7A2297DA02B8F4BA8E0"


    def test_sm3_loop(basic_loop, rand_bytes):
        sm3_hash = sm3.SM3()
        sm3_hash.start()
        msg_total = b''

        for _ in range(basic_loop):
            msg = rand_bytes(random.randint(1, 128))
            sm3_hash.update(msg)
            msg_total += msg

        print(sm3.sm3_hash(msg_total))
        assert sm3_hash.finish() == sm3.sm3_hash(msg_total)

#66C7F0F462EEEDD9D1F2D46BDC10E4E24167C4875CF2F7A2297DA02B8F4BA8E0

if __name__ == '__main__':
    from gmssl import sm3
    y = sm3.sm3_hash(b"abc")
    print(y)
