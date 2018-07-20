xor = lambda a, b:list(map(lambda x, y: x ^ y, a, b))

rotl = lambda x, n:int(int(x << n) & 0xffffffff) | int((x >> (32 - n)) & 0xffffffff)

get_uint32_be = lambda key_data:int((key_data[0] << 24) | (key_data[1] << 16) | (key_data[2] << 8) | (key_data[3]))

put_uint32_be = lambda n:[int((n>>24)&0xff), int((n>>16)&0xff), int((n>>8)&0xff), int((n)&0xff)]


def padding(text, block_byte=16, encoding='utf8'):
    """
    加密填充和解密去填充
    """

    # unicode
    if isinstance(text, str):
        text = text.encode(encoding=encoding)

    if self.mode == SM4_ENCRYPT:
        # 填充
        p_num = block_byte - (len(text) % block_byte)
        space = b''
        pad_s = (chr(p_num).encode(encoding) * p_num)
        res = space.join([text, pad_s])
    else:
        # 去填充
        p_num = text[-1]
        res = text[:-p_num]
    return res

def padding(data, block=16):
    pad = 16 - len(data) % 16
    for _ in range(16 - len(data) % 16):
        data.append(pad)
    return [for _ in range(16 - len(data) % 16)]
unpadding = lambda data: data[:data[-1]]
