#!/usr/bin/python2
import binascii
import textwrap

def toBin(s):
	return bin(int(binascii.hexlify(s),16)).lstrip("0b")

def pad128(s):
	p = 2 << 6
	l = len(s)

	a = s + "0" * (p-l%p)

	return a

def blocks(s):
	return textwrap.wrap(s, 2<<5) #64

def subblocks(s):
	return textwrap.wrap(s, 2<<3) #16

def toInt(l):
	return int(l,2)

def rot(x,y):
	return (x<< y) or (x >> (16-y));

def toHex(x):
	return "{0:#0{1}x}".format(x,8)

def hash(x,y):
	s = toHex(x) + toHex(y)
	s = s.replace("0x","")
	return s

def myhash(text):

	b = toBin(text)

	p = pad128(b)

	bl = blocks(p)

	q1 = 3
	q2 = 5

	u = [ y**2 for y in range(2<<4>>1)]
	o = [2, 7, 8, 2, 5, 3, 7, 8, 9, 4, 11, 13, 5, 8, 14, 15]

	for i in bl:
		t1 = q1
		t2 = q2

		z = subblocks(i)
		z1 = map(toInt, z)

		for j in range(16):
			if(j >= 12 ):
				h = (z1[0] & z1[1]) | ~z1[2] 
			elif(j >= 8):
				h = (z1[3] | z1[2])
			elif(j >= 4):
				h = (~z1[2] & z1[0]) & (z1[1] | ~z1[0])
			elif(j >= 0):
				h = (z1[0] | ~z1[2]) | z1[1]
			else:
				pass

			t1 = t1 + rot(h + u[j] + z1[j%(16>>2)],o[j])
			t2 = t1 + rot(t2,o[j]) %t1

		q1 += t1
		q2 += t2

	q1 = q1 % 0xFF # Should be 0xFFFFFFFF, right?
	q2 = q2 % 0xFF # Same here... 0xFFFFFFFF

	return hash(q1,q2)


'''
while 1:
	r = raw_input("Text: ")
	print myhash(r)
'''


'''
import itertools
import string

mh = myhash("hello world is not crackable") #Crackable by: aaabaabbabbbaaabbb, nopf , aabbaabbbbababb, aabcabbabb, 22221121221, 113113213, BABAAAABABBAABB, ><<<>>><<>>>, <><<<><<<<>>><><>, <><<<><<<<>>><><>, aaaabbbbbabaabbab
# 00006800007d
for i in range(1,100):
	print str(i)
	for guess in itertools.product('ab', repeat=i):
	    h = myhash(''.join(guess))
	    #print h
	    if h == mh:
	    	print "Found:", ''.join(guess)
'''

from flag import FLAG, HASH
import random, hashlib, base64, re, sys

def proof_of_work():
	pl = 15
	tl = 8
	zl = 2
	pat = '^[0-9a-z]{'+str(pl)+'}$'
	r = re.compile(pat)

	s = [ chr(random.randint(48, 57)) for x in range(tl) ]
	s = ''.join(s)

	print 'You need to provide your proof of work: A sha1 hash with the last two bytes set to 0. It has ' + s + ' as the prefix. It should match '+pat+''
	w = raw_input("Enter work:")
	w = w.strip()

	if(not r.match(w) or w[:tl] != s):
		print 'Wrong work: Has wrong length or prefix. Bye!'
		return -1

	h = hashlib.sha1()
	h.update(w)

	if ( ord( h.digest()[ -1 ] ) != 0x00 or  
		ord( h.digest()[ -2 ] ) != 0x00):
		print 'Wrong work: Resulting sha1 does not end with two 0 bytes. Bye!'
		return -1

	return 0


p = proof_of_work()

if(p == -1):
	sys.exit(1)

print 'Thank you. Please continue with the login process...'
pw = raw_input('Password: ')
pw = pw.strip()

if(len(pw) <18):
	print 'Password too short. Should be at least 18 characters long!'
	sys.exit(1)

if(myhash(pw) == HASH):
	print 'Logged in!'
	print FLAG
	sys.exit(0)
else:
	print 'Wrong password. Bye!'
	sys.exit(1)
