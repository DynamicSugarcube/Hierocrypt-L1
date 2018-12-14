import random
import libcrypt as lbcr

SBOX = (0x07, 0xFC, 0x55, 0x70, 0x98, 0x8E, 0x84, 0x4E, 0xBC, 0x75, 0xCE, 0x18, 0x02, 0xE9, 0x5D, 0x80,
        0x1C, 0x60, 0x78, 0x42, 0x9D, 0x2E, 0xF5, 0xE8, 0xC6, 0x7A, 0x2F, 0xA4, 0xB2, 0x5F, 0x19, 0x87,
        0x0B, 0x9B, 0x9C, 0xD3, 0xC3, 0x77, 0x3D, 0x6F, 0xB9, 0x2D, 0x4D, 0xF7, 0x8C, 0xA7, 0xAC, 0x17,
        0x3C, 0x5A, 0x41, 0xC9, 0x29, 0xED, 0xDE, 0x27, 0x69, 0x30, 0x72, 0xA8, 0x95, 0x3E, 0xF9, 0xD8,
        0x21, 0x8B, 0x44, 0xD7, 0x11, 0x0D, 0x48, 0xFD, 0x6A, 0x01, 0x57, 0xE5, 0xBD, 0x85, 0xEC, 0x1E,
        0x37, 0x9F, 0xB5, 0x9A, 0x7C, 0x09, 0xF1, 0xB1, 0x94, 0x81, 0x82, 0x08, 0xFB, 0xC0, 0x51, 0x0F,
        0x61, 0x7F, 0x1A, 0x56, 0x96, 0x13, 0xC1, 0x67, 0x99, 0x03, 0x5E, 0xB6, 0xCA, 0xFA, 0x9E, 0xDF,
        0xD6, 0x83, 0xCC, 0xA2, 0x12, 0x23, 0xB7, 0x65, 0xD0, 0x39, 0x7D, 0x3B, 0xD5, 0xB0, 0xAF, 0x1F,
        0x06, 0xC8, 0x34, 0xC5, 0x1B, 0x79, 0x4B, 0x66, 0xBF, 0x88, 0x4A, 0xC4, 0xEF, 0x58, 0x3F, 0x0A,
        0x2C, 0x73, 0xD1, 0xF8, 0x6B, 0xE6, 0x20, 0xB8, 0x22, 0x43, 0xB3, 0x33, 0xE7, 0xF0, 0x71, 0x7E,
        0x52, 0x89, 0x47, 0x63, 0x0E, 0x6D, 0xE3, 0xBE, 0x59, 0x64, 0xEE, 0xF6, 0x38, 0x5C, 0xF4, 0x5B,
        0x49, 0xD4, 0xE0, 0xF3, 0xBB, 0x54, 0x26, 0x2B, 0x00, 0x86, 0x90, 0xFF, 0xFE, 0xA6, 0x7B, 0x05,
        0xAD, 0x68, 0xA1, 0x10, 0xEB, 0xC7, 0xE2, 0xF2, 0x46, 0x8A, 0x6C, 0x14, 0x6E, 0xCF, 0x35, 0x45,
        0x50, 0xD2, 0x92, 0x74, 0x93, 0xE1, 0xDA, 0xAE, 0xA9, 0x53, 0xE4, 0x40, 0xCD, 0xBA, 0x97, 0xA3,
        0x91, 0x31, 0x25, 0x76, 0x36, 0x32, 0x28, 0x3A, 0x24, 0x4C, 0xDB, 0xD9, 0x8D, 0xDC, 0x62, 0x2A,
        0xEA, 0x15, 0xDD, 0xC2, 0xA5, 0x0C, 0x04, 0x1D, 0x8F, 0xCB, 0xB4, 0x4F, 0x16, 0xAB, 0xAA, 0xA0)

MDS = ((0xC4, 0x65, 0xC8, 0x8B),
       (0x8B, 0xC4, 0x65, 0xC8),
       (0xC8, 0x8B, 0xC4, 0x65),
       (0x65, 0xC8, 0x8B, 0xC4))

MDSH = ((0x5, 0x7), (0xa, 0xb))

KEY_SIZE = 128
BLOCK_SIZE = 64

primitiveGF8 = 0x163


def poly32_deg(a):
    n = -1
    while a != 0:
        n += 1
        a >>= 1
    return n


def poly32_mul(a, b):
    c = 0
    while b != 0:
        if b & 1:
            c ^= a
        b >>= 1
        a <<= 1
    return c


def poly32_mod(a, b):
    da = poly32_deg(a)
    db = poly32_deg(b)
    if (da < db):
        return a
    if (da == db):
        return a ^ b
    b <<= da - db
    t = 1 << da
    while da >= db:
        if (a & t):
            a ^= b
        b >>= 1
        t >>= 1
        da -= 1
    return a


def break_key_into_blocks(key, block_size):
    def get_block(n):
        return n % 2 ** block_size

    def rshift(n):
        return n >> block_size

    nbytes = KEY_SIZE // block_size

    blocks = []
    for n in range(nbytes):
        blocks.append(get_block(key))
        key = rshift(key)

    blocks.reverse()
    return blocks


def break_data_into_blocks(data):
    nitems = BLOCK_SIZE // 8

    data_len = len(data)
    if data_len % nitems != 0:
        nrequired = nitems - data_len % nitems
        for n in range(nrequired):
            data.append(0)
        data_len += nrequired

    blocks = []
    for n in range(0, data_len, 8):
        blocks.append(data[n:n + 8])

    return blocks


def hcryptL1_xs(data):
    def hcryptL1_mdsl(data):
        out = []
        for i in range(4):
            m = 0
            for j in range(4):
                m ^= poly32_mod(poly32_mul(MDS[i][j], data[j]), primitiveGF8)
            out.append(m)
        return out

    nitems = len(data)

    # Генерация ключа
    key = random.getrandbits(KEY_SIZE)
    key_bytes = break_key_into_blocks(key, 8)
    l_key_bytes = key_bytes[:8]
    r_key_bytes = key_bytes[8:]

    # Наложение ключа l_key_bytes
    for i in range(nitems):
        data[i] ^= l_key_bytes[i]

    # Табличная замена байтов
    for i in range(nitems):
        data[i] = SBOX[int(data[i])]

    # Умножение на матрицу mds
    ldata = hcryptL1_mdsl(data[:4])
    rdata = hcryptL1_mdsl(data[4:])
    data = ldata + rdata

    # Наложение ключа r_key_bytes
    for i in range(nitems):
        data[i] ^= r_key_bytes[i]

    # Табличная замена байтов
    for i in range(nitems):
        data[i] = SBOX[int(data[i])]

    return data


def mdsh_mul(data, x):
    out = [0 for i in range(4)]
    if x & 1 != 0:
        out[0] ^= data[0]
        out[1] ^= data[1]
        out[2] ^= data[2]
        out[3] ^= data[3]
    if x & 2 != 0:
        out[0] ^= data[1]
        out[1] ^= data[2]
        out[2] ^= data[3] ^ data[0]
        out[3] ^= data[0]
    if x & 4 != 0:
        out[0] ^= data[2]
        out[1] ^= data[3] ^ data[0]
        out[2] ^= data[0] ^ data[1]
        out[3] ^= data[1]
    if x & 8 != 0:
        out[0] ^= data[3] ^ data[0]
        out[1] ^= data[0] ^ data[1]
        out[2] ^= data[1] ^ data[2]
        out[3] ^= data[2]
    return out


def hcryptL1_mdsh(data):
    out = [[0 for j in range(4)] for i in range(2)]
    for i in range(2):
        for j in range(2):
            tmp = mdsh_mul(data[4 * j: 4 * (j + 1)], MDSH[i][j])
            for k in range(4):
                out[i][k] ^= tmp[k]
    return out[0] + out[1]


def encrypt(data):
    blocks = break_data_into_blocks(data)
    for i in range(len(blocks)):
        for r in range(5):
            hcryptL1_xs(blocks[i])
            hcryptL1_mdsh(blocks[i])
        hcryptL1_xs(blocks[i])

    out = []
    for i in range(len(blocks)):
        out += blocks[i]
    return out

def key_expansion(key):
    z=[]
    h = [0x5A827999,
         0x6ED9EBA1,
         0x8F1BBCDC,
         0xCA62C1D6,
         0xF7DEF58A]
    m5 = [[1, 0, 1, 0],
          [1, 1, 0, 1],
          [1, 1, 1, 0],
          [0, 1, 0, 1]]
    mb = [[0, 1, 0, 1],
          [1, 0, 1, 0],
          [1, 1, 0, 1],
          [1, 0, 1, 1]]
    m8 = [[1, 0, 1, 0],
          [0, 1, 0, 1],
          [0, 1, 1, 1],
          [1, 0, 1, 1]]
    ki = break_key_into_blocks(key, 32)
    x = [break_key_into_blocks(ki[i], 8) for i in range(4)]
    z[1] = ki[2]
    z[3] = lbcr.galoisMul(m5, x[1])
    for i in range(4):
        z[3][i] ^= h[0]
    z[4] = lbcr.galoisMul(mb, x[4])