Internetwache CTF 2016 
======================================

This is the Internetwache CTF 2016 repository. It contains all files, tools and notes which were used to build and host the CTF. 
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
- Blogpost: <https://en.internetwache.org/internetwache-ctf-2016-review-01-03-2016/>

# Scoreboard

The scoreboard is based on the [tinyctf-platform](https://github.com/balidani/tinyctf-platform). Check the ```README.tinyctf.md``` and ```LICENSE.tinyctf.md``` for more information. You can find our modified fork here: <https://github.com/internetwache/tinyctf-platform>

# Directory structure

The ```tasks/``` directory contains information about all challenges:

```
├── tasks 							//	Contains all tasks
│   ├── challengeXY					//	Every challenge has a separate directory
│   │   ├── code 						//	Directory with serverside code
│   │   │   ├── service.py 			//	Service
│   │   │   └── flag.py 				//	File with flag
│   │   ├── solution 					//	Directory with public information
│   │   │   ├── description.md 		//	Name and description
│   │   │   └── flag.txt 				//	Flag
│   │   └── task 						//	Directory with resources for download
│   │       └── README.txt 			// 	File with challenge hints or code
```

# Other files:

- ```tasks/checkservice.py```

A small python script/plugin for the collectd monitoring system. Checks the availability of the services.

- ```tasks/createzips.sh```

Bundles every ```tasks/<challenge>/task/``` directory into a ```static/files/<challenge>.zip```

- ```tasks/pkiller.py```

Dirty workaround script to kill long-living apache-mpm-itk subprocesses (spawned by RCE challenges)

- ```tasks/tasks.md```

An overview over all challenges' names, flags, urls, ips, ports.

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
	- 1x 1 Core, 512 mb, 20GB, 0.007$/h VM as monitor
	- 1x 4 Core, 8 gb, 80gb, 0.119$/h VM as proxy (load balancer)
		- nginx load balancer: HTTP to web1 / TCP to serv1
	- 1x 4 Core, 8 gb, 80gb, 0.119$/h VM as web1 backend
		- web50, web60, web70, web80, web90, crypto80 challenges
	- 1x 4 Core, 8 gb, 80gb, 0.119$/h VM as serv1 backend [ASLR disabled]
		- crypto70, crypto90, code50, code60, code70, code80, code90, exp50, exp60, exp70, exp80, exp90 challenges
	- 1x Floating IP pointing to proxy
	- Costs for hosting: ~20$

- Setup:
	- Monitor ==> priv. network to proxy / web1 / serv1
	- Internet ==> proxy ==> priv. network to web1 / serv1
		- Pro: Easy to scale by spawning new VMs
		- Pro: Malicious attackers can be stopped on the proxy
		- Contra: Proxy is single point of failure
	- All challenges ran as a separate user
	- All users were in the ```ctf``` group
	- Used [Daemontools](http://cr.yp.to/daemontools.html) to control services
	- Used [TCPServer](http://cr.yp.to/ucspi-tcp/tcpserver.html) to provide tcp connections for executables and scripts.
	- Used [CGroups](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Resource_Management_Guide/ch01.html) to limit resources of users from the ```ctf``` group
	- Used [Collectd](https://collectd.org/) with [CGP frontend](https://github.com/pommi/CGP) to monitor all VMs
	- Used [Let's encrypt](https://letsencrypt.org/) for SSL certificates