#!/usr/bin/python2
import os
import flag

class Randomizer:
	def __init__(self, a, c, m, s):
		self.__a = a
		self.__c = c
		self.__m = m
		self.__x = s

	def get_next(self):
		self.__x = (self.__a*self.__x + self.__c) % self.__m
		return self.__x

	def get_a(self):
		return self.__a 
	def set_a(self, a):
		self.__a = a

	def get_c(self):
		return self.__c 
	def set_c(self, c):
		self.__c = c

	def get_m(self):
		return self.__m 
	def set_m(self, m):
		self.__m = m

	def get_x(self):
		return self.__x 
	def set_x(self, x):
		self.__x = x

class Cipher:
	def __init__(self):
		self.__r = Randomizer(1664525, 1013904223, 2**32, 0)

	def encrypt(self, t):
		self.__r.set_x(t.get_k())
		ct = ""
		s = str(t)
		l = len(s)
		for c in s:
			ct += chr( ord(c) ^ (self.__r.get_next() % 2**7) )
		return ct.encode('hex')

	def decrypt(self, t, ct):
		self.__r.set_x(t.get_k())
		try:
			ct = ct.decode('hex')
			pt = ""
			for c in ct:
				pt += chr( ord(c) ^ (self.__r.get_next() % 2**7) )
			if(not "TRANSACTION" in pt):
				return None
			a = int(pt.replace("TRANSACTION:",""))
			t.set_a(a)
			return t
		except:
			return None

class Transaction:
	def __init__(self, a):
		self.__a = a
		self.__k = int(os.urandom(32).encode('hex'),16)
		self.__v = True

	def get_a(self):
		return self.__a

	def set_a(self, a):
		self.__a = a

	def get_k(self):
		return self.__k

	def set_k(self, k):
		self.__k = k

	def get_v(self):
		return self.__v

	def set_v(self, v):
		self.__v = v

	def __str__(self):
		return "TRANSACTION: " + str(self.__a)


class Account:
	def __init__(self):
		self.__m = 0
		self.__t = []
		self.__t_max = 5000

	def create_t(self, a):
		if(len(self.__t) > 20):
			return None, None
		if(a > self.__t_max):
			return None, None

		t = Transaction(a)
		self.__t.append(t)
		return t, len(self.__t) - 1

	def get_m(self):
		return self.__m

	def set_m(self, m):
		self.__m = m

	def get_t(self):
		return self.__t

	def set_t(self, t):
		self.__t = t

	def get_t_max(self):
		return self.__t_max

	def set_t_max(self, t_max):
		self.__t_max = t_max

	def add_m(self, t):
		if(not t.get_v()):
			return None
		self.__m += t.get_a()
		t.set_v(False)
		return t

	def sub_m(self, t):
		if(not t.get_v()):
			return None
		self.__m -= t.get_a()
		t.set_v(False)
		return t

A = Account()
C = Cipher()

def help():
	return '''
Possible commands:
	help - Prints this message
	create <a> - Creates a new transaction with amount <a>
	complete <tid> <hash> - Completes a transaction to the current account. <tid> is the transaction ID to use and <hash> the verification hash.
'''

print 'WELCOME TO THE BANK BACKEND!'
print help()
while(len(A.get_t()) <= 20):
	print 'Your balance: {}, {} transactions left.'.format(A.get_m(), 20 - len(A.get_t()))
	cmd = raw_input("Command: ").strip()

	if(cmd == "help"):
		print help()
	elif("create" in cmd):
		try:
			a = int(cmd.replace("create ",""))
			t, i = A.create_t(a)
			if t is None:
				print 'Too many transactions or amount too big!'
				continue
			tc = C.encrypt(t)
			print "Transaction #{} over {} initiated. Please complete it using the verification code: {}".format(i, t.get_a(), tc)

		except Exception as e:
			print 'Oops, something went wrong.'
	elif("complete" in cmd):
		try:
			text = cmd.replace("complete ","").split(" ")
			t = int(text[0])
			h = text[1]
			if(len(A.get_t()) < t):
				print 'Wrong transaction ID'
				continue
			if(not len(h) in range(28, 35)):
				print 'Wrong verification length'
				continue
			tn = A.get_t()[t]
			tn = C.decrypt(tn, h)
			if(tn is None):
				print 'Oops, verification failed!'
				continue
			r = A.add_m(tn)
			if(r is None):
				print 'You cannot complete a transaction twice!'
			print 'Transaction completed!'
		except:
			print 'Oops, something went wrong.'

	if(A.get_m() >= 10**6):
		print flag.FLAG