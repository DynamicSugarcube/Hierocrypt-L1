import random as rnd

PRIMITIVE_GF8 = 0x163 # x^8 + x^6 + x^5 + x + 1

# Умножение в поле GF(2^8)
def poly_mul(a, b):
	c = 0
	while b != 0:
		if b & 1:
			c ^= a
		b >>= 1
		a <<= 1
	return c

# Нахождение остатка от деления в поле GF(2^8)
def poly_mod(a, b):
	def poly_deg(a):
		n = -1
		while a != 0:
			n += 1
			a >>= 1
		return n

	da = poly_deg(a)
	db = poly_deg(b)
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
    
# Тест Ферма на простоту числа n		
def fermat_test(n):
    a = rnd.randint(2, n - 1)
    return pow(a, n - 1, n) == 1


# Тест числа n на простоту
# Выполняет тест Ферма для числа n ntimes раз	
def is_prime(n, ntimes):
    for test in range(ntimes):
        if not fermat_test(n):
            return False
    return True


# Возвращает nrequired самых больших простых чисел
# из диапазона (2, max_num);
# По умолчанию required=-1 значит, что возвращаются 
# все простые числа из данного диапазона
def find_primes(max_num, max_test, nrequired=-1):
    primes = []
    for num in range(max_num, 2, -1):
        if is_prime(num, max_test):
            primes.append(num)
        if nrequired >= 0 and len(primes) >= nrequired:
            break
    return primes


# Генератор СЧ
def random_generator(x):
	def f1(x):
		a = 4
		b = 101
		return a * x + b
	def f2(x):
		a = 3
		b = 92
		return x // a + b

	MAX_RAND = 2**128 - 1
	MIN_RAND = 2**127
	NTIMES = 256

	arr = []
	for n in range(NTIMES):
		if n % 2 == 0:
			x = f1(x)
		else:
			x = f2(x)
		if x < MIN_RAND:
			x = f1(x)
		if x > MAX_RAND:
			x = f2(x)
		arr.append(x)

	return arr[rnd.randint(NTIMES // 2, NTIMES - 1)]
