import psutil
import time 

while True:
	for p in psutil.process_iter():
		if not "web" in p.username():
			continue
		now = time.time()
		if now > p.create_time() + 10:
			print p
			p.kill()
	time.sleep(2)