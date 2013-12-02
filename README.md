open-nic
========

Use OpenNIC DNS right now

Current status as of 1st nov 13:
- works fine on Debian
- does not work on Mint/Ubuntu (runs as intented but for some reason it has no effect -see below)

What is OpenNIC and why should I use it ?
=================

The OpenNIC project is an alternative DNS provider. Users of the
OpenNIC DNS servers are able to resolve all existing ICANN top-level
domains (TLD) as well as their own.

You should use it if you're concerned about censorship, if you don't
want your internet provider to know every site you visit, if you want
to support independant projects, and maybe if you want to access
.geek, .indy, .free, .ing… websites, that are only served by OpenNIC.

http://www.opennicproject.org/

https://en.wikipedia.org/wiki/OpenNIC


How to use this script
======================

The scripts depends on the **resolvconf** package (by default in
Mint/Ubuntu) and the **BeautifulSoup4** python library (by default ?).
To install the dependencies:

     sudo apt-get install resolvconf
     sudo apt-get install python-pip && sudo pip install BeautifulSoup4

Download the script and call:

     sudo python opennic-set.py

Or run:

    wget https://raw.github.com/vindarel/open-nic/master/opennic-set.py && sudo python opennic-set.py

Now you will keep using the same DNS providers for all the usual
websites, but you will also be able to access OpenNIC's TLDs. If you
would like to always use OpenNIC's servers, then you have to copy
`/etc/resolvconf/resolv.conf.d/tail` to `…/head`.

You should now be able to access this website:
http://wiki.opennic.glue/SponsoredTLDs). You can also test with:

     python opennic-set.py --test

What the script does
===========

More precisely, the script does the following:
- it retrieves which are the nearest OpenNIC DNS servers from your
  location thanks to the project's homepage (if their site isn't
  reachable it takes 3 servers by default)
- it adds them to the configuration file used by resolvconf (`/etc/resolvconf/resolv.conf.d/tail`) (a backup is made)
- it runs `resolvconf -u` to update the configuration (you can see changes in `/etc/resolv.conf`)
- it tests wether we can access opennic's TLDs.

Every remark welcomed.

Known issues
============

It runs as expected in Mint/Ubunt but has no effect. The bug is reproductible:
- add the line
nameserver 185.19.105.6 # openNic
at the beginning of `/etc/resolvconf/resolv.conf.d/head`
- execute sudo resolvconf -u
- you *should* be able to access the url given above, but you can't. With Debian it's ok.

More info
=========
- on network conf: http://www.linux-france.org/prj/edu/archinet/systeme/ch03s02.html
