#!/usr/bin/python2

import os, time, sys, socket

INTERVAL = float(os.environ['COLLECTD_INTERVAL'])
HOSTNAME = os.environ['COLLECTD_HOSTNAME']

if not INTERVAL or not HOSTNAME:
	os.exit(1)

if INTERVAL < 10:
	os.exit(1)

HOST = "127.0.0.1"
SERVICE = sys.argv[1]
PORT = int(sys.argv[2])
CONTENT = sys.argv[3]

if not PORT in [10009, 10061, 11027, 11059, 11071, 11117, 11491, 12037, 12049, 12157, 12377, 12589]:
	os.exit(1)

def do_check():
	s = socket.socket(
	    socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST,PORT))
	text = s.recv(len(CONTENT)+1)
	s.close()
	if CONTENT in text:
		return 0
	return 1

while True:
	st = time.time()
	iserror = do_check()
	duration = int((time.time() - st) * 1000)
	print "PUTVAL {}/services-{}/gauge-con_error {}:{}".format(HOSTNAME, SERVICE, int(st), iserror)
	print "PUTVAL {}/services-{}/gauge-con_ms {}:{}".format(HOSTNAME, SERVICE, int(st), duration)
	sys.stdout.flush()
	time.sleep(INTERVAL)