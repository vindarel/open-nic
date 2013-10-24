#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from bs4 import BeautifulSoup
except ImportError:
    print 'you need to install BeautifulSoup4: '
    print "sudo pip install BeautifulSoup4"
    exit(1)
import re
import os
import sys
import shutil
import platform
import argparse
import subprocess
import urllib2

"""
Use dns servers of the open-nic project.
Get the nearest dns servers and insert them into your configuration.

usage: sudo python opennic-set.py

Requirements:
apt-get install resolvconf # installed in Ubuntu ?
apt-get install python-pip && pip install BeautifulSoup4
"""
# Better explanations:
# http://www.stgraber.org/2012/02/24/dns-in-ubuntu-12-04/
# http://askubuntu.com/questions/130452/how-do-i-add-a-dns-server-via-resolv-conf
# dhclient.conf is outdated: http://raamdev.com/2009/configuring-static-dns-with-dhcp-on-debianubuntu/ -> outdated !

# maybe /etc/resolvconf/resolv.conf.d/head http://askubuntu.com/questions/2321/what-is-the-proper-way-to-change-the-dns-ip
DEBIAN_CONF = "/etc/resolvconf/resolv.conf.d/tail"
# UBUNTU_CONF = "/etc/resolvconf/resolv.conf.d/tail"

# http://www.opennicproject.org/geoip/geotxt4.php = working resolv.conf (overwriten)

RESOLVCONF = "/sbin/resolvconf"
DEFAULT_DNS = ["185.19.105.6", "216.87.84.211",] #UK and US

# def getConf():
#     """
#     Set conf file depending on distro
#     """
#     distro, version, d_name = platform.linux_distribution()
#     distro = distro.lower()
#     if distro == "ubuntu":
#         return UBUNTU_CONF
#     elif distro == "debian":
#         return DEBIAN_CONF
#     else:
#         print "We didn't recognize your GNU/Linux distro, so… let's assume you are compatible with Ubuntu !"
#         return UBUNTU_CONF


def getDnsList():
    """Gets your nearest OpenNic servers from their page
    (http://www.opennicproject.org/nearest-servers/).

    If this service isn't working, uses default servers.

    returns a list of IP addresses.
    """
    url = "http://www.opennicproject.org/nearest-servers/"
    r = urllib2.urlopen(url)
    nic = BeautifulSoup(r.read())
    assert nic
    nearest = nic.find_all('div', class_='post-entry')
    assert nearest[0]
    dns_text = nearest[0].find('p')
    assert dns_text.text
    dns_list = re.findall('\d+\.\d+\.\d+\.\d+', dns_text.text)
    if not dns_list:
        print "Warning: we couldn't get the nearest opennic servers from you. Using default servers (UK and US)"
        dns_list = DEFAULT_DNS
    return dns_list

def updateResolvconf():
    """resolvconf -u
    """
    print "Updating configuration…",
    subprocess.Popen(['resolvconf', '-u'])
    print " done."

def testOpennic(url="http://wiki.opennic.glue/SponsoredTLDs"):
    """Tests if we can access opennic TLDs
    """
    print "Testing… ",
    try:
        ret = urllib2.urlopen(url)
        if not ret:
            print "test successful: we can access opennic's %s" % (url,)
            return ret
        return 0
    except:
        print "test FAILED: we can't access opennic's domains (trying %s)" % (url,)
        return 1

def editConf(dns_list, conf):
    """Writes the given dns servers to the given file.
    """
    BACK = conf + ".back"
    if os.path.exists(conf):
        if not os.path.exists(BACK):
            shutil.copyfile(conf, BACK)
    else:
    	print "Configuration file %s not found. Did you install the 'resolvconf' package ? (sudo apt-get install resolvconf)" % (conf,)
	exit(1)

    w = "\n".join("nameserver " + dns for dns in dns_list)

    with open(conf, 'a+') as f:
        print "we  add the lines:\n" +  w + " to the file " + conf
        print "we saved the original conf file, so if you notice any connection pb, you can still put it back"
        f.write(w)

def main(*args):
    # CONF = getConf()
    CONF = DEBIAN_CONF

    dns_list = getDnsList()
    print "nearest dns list: ", dns_list

    #TODO: check the addresses are not on the same network
    editConf(dns_list, CONF)
    updateResolvconf()
    testOpennic()


#todo: proposer un «undo»: remettre le .back en place

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Use an Opennic DNS server. Usage: sudo python opennic-set.py")
    parser.add_argument("-t", "--test", action='store_true',
                    help="test if we can access an opennic's TLD")

    args = parser.parse_args()
    if args.test:
        exit(testOpennic())

    exit(main(sys.argv[1:]))
