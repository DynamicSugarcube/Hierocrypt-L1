import random
import libcrypt as lc

# Таблица замены при шифровании
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

# Константные матрицы, используемые при шифровании
MDS = ((0xC4, 0x65, 0xC8, 0x8B),
       (0x8B, 0xC4, 0x65, 0xC8),
       (0xC8, 0x8B, 0xC4, 0x65),
       (0x65, 0xC8, 0x8B, 0xC4))

MDSH = ((1, 0, 1, 0, 1, 1, 1, 0),
		(1, 1, 0, 1, 1, 1, 1, 1),
		(1, 1, 1, 0, 0, 1, 1, 1),
		(0, 1, 0, 1, 1, 1, 0, 1),
		(1, 1, 0, 1, 0, 1, 0, 1),
		(1, 1, 1, 0, 1, 0, 1, 0),
		(1, 1, 1, 1, 1, 1, 0, 1),
		(1, 0, 1, 0, 1, 0, 1, 1))
			
# Константные матрицы, используемые при расширении ключа			
HCONSTS = (0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xCA62C1D6, 0xF7DEF58A)

M5 = ((1, 0, 1, 0), (1, 1, 0, 1),
	  (1, 1, 1, 0), (0, 1, 0, 1))

MB = ((0, 1, 0, 1), (1, 0, 1, 0),
	  (1, 1, 0, 1), (1, 0, 1, 1))

M8 = ((1, 0, 1, 0), (0, 1, 0, 1),
	  (0, 1, 1, 1), (1, 0, 1, 1))

KEY_SIZE = 128
BLOCK_SIZE = 64

def break_key_into_blocks(key, block_size, key_size):
    def get_right_block(n):
        return n % 2 ** block_size

    def rshift(n):
        return n >> block_size

    nbytes = key_size // block_size

    blocks = []
    for n in range(nbytes):
        blocks.append(get_right_block(key))
        key = rshift(key)

    blocks.reverse()
    return blocks


def break_data_into_blocks(data):
	items_per_block = BLOCK_SIZE // 8

	data_len = len(data)
	if data_len % items_per_block != 0:
		nrequired = items_per_block - data_len % items_per_block
		for n in range(nrequired):
			data.append(0)
		data_len += nrequired

	blocks = []
	for n in range(0, data_len, 8):
		blocks.append(data[n:n + 8])

	return blocks
    
def glue_bytes(byte_arr):
    res = 0
    byte_arr.reverse()
    for i in range(len(byte_arr)):
        res += byte_arr[i] * 2**(8 * i)
    return res

def matrix_mul(data, mul_matrix):
        out = []
        n = len(mul_matrix)
        for i in range(n):
            m = 0
            for j in range(n):
                m ^= lc.poly_mod(lc.poly_mul(mul_matrix[i][j], data[j]), lc.PRIMITIVE_GF8)
            out.append(m)
        return out
        
def key_expansion(key):
    def P5(x):
        blocks = break_key_into_blocks(x, 8, 32)
        blocks = matrix_mul(blocks, M5)
        return glue_bytes(blocks)

    def PB(x):
        blocks = break_key_into_blocks(x, 8, 32)
        blocks = matrix_mul(blocks, M8)
        return glue_bytes(blocks)

    def F(x):
        blocks = break_key_into_blocks(x, 8, 32)
        blocks = [SBOX[blocks[i]] for i in range(len(blocks))]
        blocks = matrix_mul(blocks, M8)
        return glue_bytes(blocks)

    def P16(x):
        t1 = matrix_mul(x, MB)
        t2 = matrix_mul(x, M5)
        return glue_bytes(t1), glue_bytes(t2)

    # Генерация промежуточного ключа
    key_blocks = break_key_into_blocks(key, 32, KEY_SIZE)
    z3 = P5(key_blocks[2]) ^ HCONSTS[0]
    z4 = PB(key_blocks[3])
    z1 = key_blocks[1]
    z2 = key_blocks[0] ^ F(key_blocks[1] ^ z3)
    
    # Вычисление расширенных ключей
    out_keys = [0 for i in range(7)]

    x1, x2, x3, x4 = z1, z2, z3, z4
    for i in range(4):
        y3 = P5(x3) ^ HCONSTS[i + 1]
        y4 = PB(x4)
        y1 = x2
        y2 = x1 ^ F(x2 ^ z3)

        k11 = y2
        k12 = y2 ^ x1 ^ y3
        k21 = y2 ^ x1 ^ y4
        k22 = y1 ^ y4

        out_keys[i] = glue_bytes([k11, k21, k21, k22])

        x1, x2, x3, x4 = y1, y2, y3, y4

    for i in range(4, 7):
        out_keys[i] = out_keys[6 - i]

    return out_keys
    	
def encrypt(data, key):
	def XS(block, round_key):
		nitems = len(block)

		key_bytes = break_key_into_blocks(round_key, 8, KEY_SIZE)
		l_key_bytes = key_bytes[:8]
		r_key_bytes = key_bytes[8:]

		for i in range(nitems):
			block[i] ^= l_key_bytes[i]

		for i in range(nitems):
			block[i] = SBOX[int(block[i])]

		lblock = matrix_mul(block[:4], MDS)
		rblock = matrix_mul(block[4:], MDS)
		block = lblock + rblock

		for i in range(nitems):
			block[i] ^= r_key_bytes[i]
			
		for i in range(nitems):
			block[i] = SBOX[int(block[i])]

		return block
	
	def PH(block):
		return matrix_mul(block, MDSH)
		
	def final_key(block, key):
		nitems = len(block)
		
		key_bytes = break_key_into_blocks(key, 8, KEY_SIZE)[:8]
		for i in range(nitems):
			block[i] ^= key_bytes[i]
			
		return block

	round_keys = key_expansion(key)
	
	blocks = break_data_into_blocks(data)
	for i in range(len(blocks)):
		for r in range(5):
			blocks[i] = XS(blocks[i], round_keys[r])
			blocks[i] = PH(blocks[i])
		blocks[i] = XS(blocks[i], round_keys[-2])
		blocks[i] = final_key(blocks[i], round_keys[-1])
		
	out = []
	for i in range(len(blocks)):
		out += blocks[i]
	return out
