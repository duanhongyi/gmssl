from gmssl import sm3, func

if __name__ == '__main__':
    y = sm3.sm3_hash(func.bytes_to_list(b"abc"))
    print(y)
