import math
import random
import operator
import functools

# Python 2 and 3 compatibility
try:
	# We're in Python 2, redefine range() and input()
	range = xrange
	input = raw_input
except NameError:
	# We're in Python 3, get reduce() from functools
	reduce = functools.reduce

class cache(object):
	"""A cache for functions. To use, define function like this:
	
	@cache
	def foo(bar):
		pass
	
	"""
	# This thing eats docstrings for breakfast
	# I read a way to fix that on the internet, and then immediately forgot
	# One day I'll find it again
	
	def __init__(self, f):
		self.f = f
		self.c = {}
	
	def __call__(self, *args):
		if args not in self.c:
			self.c[args] = self.f(*args)
		return self.c[args]

@cache
def is_prime(n):
	"""Returns True if n is prime, else False"""
	if n < 2: return False
	if not n % 2: return n == 2
	for i in range(3, int(math.sqrt(n))+1, 2):
		if not n % i: return False
	return True

def prime_gen(n=2, max=float('inf')):
	"""Yields all primes below `max`."""
	# One day I'll get off my ass and write a Sieve of Eratosthenes
	if not n % 2:
		if n == 2:
			yield 2
		n += 1
	while n < max:
		if is_prime(n):
			yield n
		n += 2

@cache
def nth_prime(n):
	"""Returns the 1-indexed nth_prime"""
	if n == 1:
		return 2
	
	n -= 1 # 1-indexing is hard you guys
	a = 1
	while n:
		a += 2
		if is_prime(a):
			n -= 1
	return a

@cache
def factors(n):
	"""Returns a set of all factors of n, including 1 and itself"""
	# i got this off the internet and have only a rough idea of how it works
	# but it's fast so lmao who cares
	return set(reduce(list.__add__,([i,n//i]for i in range(1,int(math.sqrt(n))+1)if not n%i)))

def weighted_rng(weights, values):
	"""Input: A list of weights and a list of values. Weights are ints, higher =
	more commonly chosen. Each weight is associated with the value that shares
	its index.
	   Output: One element from values, chosen at random. A higher weight makes a
	value more likely to be chosen.
	"""
	assert(len(weights) == len(values))

	if not weights:
		raise IndexError('No values in lists')
	
	# If the weight is 0 it can't be chosen anyway	
	while 0 in weights:
		values.pop(weights.index(0))
		weights.remove(0)
		
	if not weights:
		raise IndexError('No values in lists after stripping zeroes')
	
	# Convert the list of weights to a list of ranges
	# e.g. [5,5,10,1] -> [5, 10, 20, 21]
	for i in range(1, len(weights)):
		weights[i] += weights[i-1]
	
	n = random.randint(1, max(weights))
	
	# Return the value assosiated with the range the random number landed in
	return values[weights.index(min(filter(lambda i: i >= n, weights)))]

def product(l):
	"""Returns the product of all elements in the list"""
	return reduce(operator.mul, l, 1)

def input_gen(skip_line=False):
	"""Yield each line in stdin. Setting skip_line to True ignores the first line
	from stdin, then yields the rest.
	"""
	if skip_line:
		input()
	while True:
		i = input()
		if i:
			yield i
		else:
			break

if __name__ == '__main__':
	print ('You aren\'t using this right! Try adding this file to your '
	       'PYTHONPATH and putting\n\n	from toolbox import *\n\nat the top of'
	       'another python program.')
