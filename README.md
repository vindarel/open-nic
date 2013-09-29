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

Simply call
    python open-nic-get.py
(you should ensure the DNS servers are not in the same location)

it will configure your configuration file with the three DNS servers
that suit you best. They are taken from their page: http://www.opennicproject.org/nearest-servers/

A restart may be needed.

You can undo the operation:
    python open-nic-undo.py