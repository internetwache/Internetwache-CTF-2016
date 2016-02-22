Internetwache CTF 2016 
======================================

The Internetwache CTF 2016 repository. This repository contains all files, tools and notes which were used to build and host the CTF. 
The ```ctf.db``` contains the final scoreboard information. 

# CTF Details

- Date: 20 Feb, 12:00 CET — 22 Feb, 00:00 CET
- Ctfime.org: <https://ctftime.org/event/290>
- Url: <https://ctf.internetwache.org>
- Registered teams: ~1500 (~650 solved at least one challenge)
- Challenges written by: [@gehaxelt](https://twitter.com/gehaxelt)
- Twitter: [@internetwache](https://twitter.com/internetwache)
- IRC: [#iwctf @ freenode.net](https://webchat.freenode.net/?channels=%23iwctf)
- Writeups: [Ctftime.org](https://ctftime.org/event/290/tasks/) or [CTF writeups](https://github.com/ctfs/write-ups-2016/tree/master/internetwache-ctf-2016)
- Prizes: None

# Scoreboard

The scoreboard is based on the tinyctf-platform. Check the ```README.tinyctf.md``` and ```LICENSE.tinyctf.md``` for more information.

# Directory structure

The most interesting directory is ```tasks/```:

```
├── tasks 							//	Directory with all tasks
│   ├── challengeXY					//	Directory for a challenge
│   │   ├── code 					//	Directory for serverside code
│   │   │   ├── service.py 			//	Service for this challenge
│   │   │   └── flag.py 			//	File with flag
│   │   ├── solution 				//	Directory for public information
│   │   │   ├── description.md 		//	Name and description of challenge
│   │   │   └── flag.txt 			//	Flag of challenge
│   │   └── task 					//	Directory with files for download
│   │       └── README.txt 			// 	File with challenge hints/code
```

# Other files:

- ```tasks/checkservice.py```

A small python script/plugin for the collectd monitoring system. Checks the availability of the services.

- ```tasks/createzips.sh```

Bundles every ```tasks/<challenge>/task/``` directory into a ```static/files/<challenge>.zip```

- ```tasks/pkiller.py```

Dirty workaround script to kill long-living apache-mpm-itk subprocesses (spawned by RCE challenges)

- ```tasks/tasks.md```

An overview over all challenges' name, flag, url, ip, port.

- ```configs/etc/cgconfig.conf```

Configuration file for Cgroups. The group ```ctf``` had limited I/O, memory and CPU shares. 

- ```configs/etc/cgrules.conf```

Configuration file for Cgroups. Assigns the rule groups to system groups.

- ```configs/etc/iptables/```

Iptables rules for the VMs.

- ```configs/etc/nginx/```

Nginx config for load balancing HTTP and TCP services.

- ```configs/etc/service/```

Daemontools services for all challenges/tools.

# Hosting details:

- 4 VMs from Digitalocean.com in AMS3 datacenter, based on Debian 8 x64, private networking enabled
	- 1x 1 Core, 512 mb, 20GB, 0.007$/h Box as monitor
	- 1x 4 Core, 8 gb, 80gb, 0.119$/h Box as proxy (load balancer)
		- nginx load balancer: HTTP to web1 / TCP to serv1
	- 1x 4 Core, 8 gb, 80gb, 0.119$/h Box as web1 backend
		- web50, web60, web70, web80, web90, crypto80 challenges
	- 1x 4 Core, 8 gb, 80gb, 0.119$/h Box as serv1 backend [ASLR disabled]
		- crypto70, crypto90, code50, code60, code70, code80, code90, exp50, exp60, exp70, exp80, exp90 challenges
	- 1x Floating IP pointing to proxy

- Setup:
	- Monitor ==> Priv. Network to proxy / web1 / serv1
	- Internet ==> proxy ==> Priv. Network to web1 / serv1
		- Pro: Easy scalable by spawning new VMs
		- Pro: Bad attackers easily stoppable on the proxy
		- Contra: Single point of failure (Proxy)
	- All challenges ran as a separate user
	- All users were in the ```ctf``` group
	- Used [Daemontools](http://cr.yp.to/daemontools.html) to easily control services
	- Used [TCPServer](http://cr.yp.to/ucspi-tcp/tcpserver.html) to provide tcp connection for executable and scripts.
	- Used [CGroups](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Resource_Management_Guide/ch01.html) to limit service-users resources
	- Used [Collectd](https://collectd.org/) with [CGP frontend](https://github.com/pommi/CGP) for monitoring the VMs
	- Used [Let's encrypt](https://letsencrypt.org/) for SSL certificates