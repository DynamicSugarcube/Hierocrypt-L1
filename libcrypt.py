import random as rnd

simple_fermat_nums = (3, 17, 257, 65537)

# Обобщённый алгоритм Евклида
# Возвращает НОД(a, b) и коэффициенты Безу
def expanded_gcd(a, b):
    a0, a1 = a, b
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    
    while a1 != 0:
        q = a0 // a1
        a0, a1 = a1, a0 - q * a1
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
        
    return (a0, x0, y0)
	
# Выполняет быстрое возведение в степень exp
# числа base по модулю m
def expmod(base, exp, m):
	if exp == 0:
		return 1
	elif exp%2 == 0:
		return (expmod(base, exp//2, m))**2 % m
	else:
		return (base * expmod(base, exp-1, m)) % m
		
# Тест Ферма на простоту числа n		
def fermat_test(n):
	a = rnd.randint(2, n-1)
	return expmod(a, n-1, n) == 1
	
# Тест числа n на простоту
# Выполняет тест Ферма для числа n max_test раз	
def is_prime(n, max_test):
    for test in range(max_test):
        if not fermat_test(n):
            return False
    return True

# Возвращает required самых больших простых чисел
# из диапазона (2, max_num);
# По умолчанию required=-1 значит, что возвращаются 
# все простые числа из данного диапазона
def find_primes(max_num, max_test, required=-1):
	primes = []
	for num in range(max_num, 2, -1):
		if is_prime(num, max_test):
			primes.append(num)
		if required >= 0 and len(primes) >= required:
			break
	return primes
# Генератор СЧ

# Меняет местами значения в массиве
# (просто чтобы несколько раз вручную не прописывать)

def replace(s, i, j):
	x = s[i]
	s[i] = s[j]
	s[j] = x


# Генерация массива чисел
# от 0 до 255 с перестановкой
# в key передается изначальный ключ (массивом)

def s_gen(key, key_size):
	s = []
	j = 0
	s = [i for i in range(0, 256)]
	for i in range(0, 255):
		j = (j + s[i] + key[i % key_size]) % 256
		replace(s, i, j)
	return s


# Генерация ключа
# Сначала нужно сгенерировать массив чисел

def keygen(s):
	i = 0
	j = 0
	x = 0
	new_key = ''
	while len(new_key) < 256:
		i = (i + 1) % 256
		j = (j + s[i]) % 256
		replace(s, i, j)
		temp = (s[i] + s[j]) % 256
		new_key += str(temp)
	return int(new_key)
