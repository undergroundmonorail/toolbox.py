#!/bin/python2

import math
import random

class cache(object):
	"""A cache for functions. To use, define function like this:
	
	@cache
	def foo(bar):
		pass
	
	"""
	c = {}
	
	def __init__(self, f):
		self.f = f
	
	def __call__(self, *args):
		if (self.f, args) not in self.c:
			self.c[(self.f, args)] = self.f(*args)
		return self.c[(self.f, args)]

@cache
def is_prime(n):
	"""Returns True if n is prime, else False"""
	if n < 2: return False
	if not n % 2: return n == 2
	for i in xrange(3, int(math.sqrt(n))+1, 2):
		if not n % i: return False
	return True

def prime_gen(n=2, max=float('inf')):
	if n == 2:
		yield 2
		n = 3
	while n < max:
		if is_prime(n):
			yield n
		n += 2

@cache
def nth_prime(n):
	a = 1
	while n:
		a += 1
		if is_prime(a):
			n -= 1
	return a

@cache
def factors(n):
	"""Returns a set of all factors of n, including 1 and itself"""
	return set(reduce(list.__add__,([i,n/i]for i in xrange(1,int(math.sqrt(n))+1)if not n%i)))

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

	while 0 in weights:
		values.pop(weights.index(0))
		weights.remove(0)
		
	if not weights:
		raise IndexError('No values in lists after stripping zeroes')
	
	for i in xrange(1, len(weights)):
		weights[i] += weights[i-1]
	
	n = random.randint(1, max(weights))
	
	return values[weights.index(min(filter(lambda i: i >= n, weights)))]

if __name__ == '__main__':
	print ('You aren\'t using this right! Try adding this file to your '
	       'PYTHONPATH and putting\n\n	from toolbox import *\n\nat the top of'
	       'another python program.')
