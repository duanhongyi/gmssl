from gmssl import sm3, func

if __name__ == '__main__':
    x = "0123456789abcdef"
    print(x)
    y = sm3.sm3_kdf(x.encode("utf-8"),64)
    print(y)
    z = sm3.sm3_kdf(x.encode("utf-8"),72)
    print(z)
