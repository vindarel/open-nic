open-nic
========

Use open-nic DNS right now

What is open-nic and why should I use it ?
=================
The Opennic project is an alternative DNS provider.

You should use it if you're concerned about censorship, if you don't
want your internet provider to know every site you visit, if you want
to support independant projects, maybe if you want to access .geek,
.indy, .free and other sites.

http://www.opennicproject.org/

https://en.wikipedia.org/wiki/OpenNIC


How to use this script
======================

The scripts depends on resolvconf and BeautifulSoup4 (by default in Ubuntu ?).
Install the dependencies:

     sudo apt-get install resolvconf
     sudo apt-get install python-pip && sudo pip install BeautifulSoup4

Simply call

     python opennic-set.py

it will configure your configuration file with the three DNS servers
that suit you best. They are taken from their page: http://www.opennicproject.org/nearest-servers/
(you should ensure the DNS servers are not in the same location)

To check if the script worked, try to access a site which can only be resolved by opennic (like http://www. ), or just run

     python opennic-set.py --test

More precisely, the script does the following:
- it retrieves which are the nearest opennic DNS servers from your location (if there's a problem, takes 3 by default)
- it adds them to the configuration file used by resolvconf (/etc/resolvconf.d/tail)
- it runs resolvconf -u to update 
- it tests wether we can access opennic's TLDs.

Every remark welcomed !

More info
=========
- on network conf: http://www.linux-france.org/prj/edu/archinet/systeme/ch03s02.html
