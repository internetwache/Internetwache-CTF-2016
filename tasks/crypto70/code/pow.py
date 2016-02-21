def pow(proof):
	import itertools
	import hashlib
	charset = ''.join( [ chr( x ) for x in xrange( 97, 122 ) ] )  
	found = False  
	for comb in itertools.combinations( charset, 7 ):  
		test = proof + ''.join( comb )  
		ha=hashlib.sha1()  
		ha.update( test )  
		if ( ord( ha.digest()[ -1 ] ) == 0x00 and  
			ord( ha.digest()[ -2 ] ) == 0x00):  
			found = True  
			break
	if found:
		return test
	else:
		return "not found"