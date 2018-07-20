xor = lambda a, b:list(map(lambda x, y: x ^ y, a, b))

rotl = lambda x, n:int(int(x << n) & 0xffffffff) | int((x >> (32 - n)) & 0xffffffff)

get_uint32_be = lambda key_data:int((key_data[0] << 24) | (key_data[1] << 16) | (key_data[2] << 8) | (key_data[3]))

put_uint32_be = lambda n:[int((n>>24)&0xff), int((n>>16)&0xff), int((n>>8)&0xff), int((n)&0xff)]

padding = lambda data, block=16: data + [(16 - len(data) % block)for _ in range(16 - len(data) % block)]

unpadding = lambda data: data[:-data[-1]]

list_to_str = lambda data: ''.join([chr(i) for i in data])

str_to_list = lambda data: [ord(i) for i in data]
