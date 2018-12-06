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
