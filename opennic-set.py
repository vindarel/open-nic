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

Requirements (on Debian):
apt-get install resolvconf # installed in Ubuntu
apt-get install python-pip && pip install BeautifulSoup4

Full information: https://github.com/vindarel/open-nic
"""
DIR_RESOLVCONF = "/etc/resolvconf/resolv.conf.d/"
DEBIAN_CONF = DIR_RESOLVCONF + "tail"
# UBUNTU_CONF = "/etc/resolvconf/resolv.conf.d/tail"

# http://www.opennicproject.org/geoip/geotxt4.php = working resolv.conf (overwriten)

RESOLVCONF = "/sbin/resolvconf"
DEFAULT_DNS = ["185.19.105.6", "216.87.84.211",] #UK and US
MAX_SERVERS = 3
BACK_SUFFIX = ".opennicset-back"

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
    """Gets your nearest openNIC servers from their page
    (http://www.opennicproject.org/nearest-servers/).

    If this service isn't working, uses default servers.

    returns a list of IP addresses.
    """
    url = "http://www.opennicproject.org/nearest-servers/"
    print "Connecting to %s..." % (url,)
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
            print "test SUCCESSFUL: we can access opennic's %s" % (url,)
            return ret
        return 0
    except:
        print "test FAILED: we can't access opennic's domains (trying %s)" % (url,)
        return 1

def maxServersExceeded(lines):
    nb_servers = 0
    for l in lines:
        if l.startswith("nameserver"):
            nb_servers += 1
    return nb_servers >= MAX_SERVERS


def editConf(dns_list, conf):
    """Writes the given dns servers to the given file.
    """
    back = conf + BACK_SUFFIX
    if os.path.exists(conf):
        if not os.path.exists(back):
            shutil.copyfile(conf, back)
    else:
        # resolvconf can be installed but …/tail not existing
        base = conf.replace('/tail', '/base')
        if os.path.exists(base):
            # create and leave
            open(conf, 'w').close()
        else:
            print "%s file not found. Did you install resolvconf ?" % (conf,)

    # if /tail already has more than 3 or 6? addresses, ours will be ignored (system limitation)
    # Print a nice message.
    with open(conf, 'r') as f:
        lines = f.readlines()
    if maxServersExceeded(lines):
        print """There is more than %s servers in %s, so ours will be ignored. You can
        still put one in /head""" % (MAX_SERVERS, conf)

    w = " # openNIC\n".join("nameserver " + dns for dns in dns_list)

    with open(conf, 'a+') as f:
        print "we  add the lines:\n" +  w + "\nto the file " + conf
        print "We saved the original configuration file, so if you notice any connection pb, you can still put it back"
        import ipdb; ipdb.set_trace()
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


def undo(conf_dir):
    """Put back the original configuration files."""
    files = ["tail", "head"]
    has_backup = False
    for f in files:
        f_path = conf_dir + f
        back = conf_dir + f + BACK_SUFFIX
        if os.path.exists(back):
            has_backup = True
            shutil.copyfile(back, f_path)
            print "backup of %s restored." % (f_path,)
            os.remove(back)

    if not has_backup:
        print "no backup found in %s" % (conf_dir,)

    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Use an Opennic DNS server. Usage: sudo python opennic-set.py")
    parser.add_argument("-t", "--test", action='store_true',
                    help="test if we can access an opennic's TLD")
    parser.add_argument("-u", "--undo", action='store_true',
                    help="put back the configuration files you had before starting playing with opennic-set.")

    args = parser.parse_args()
    if args.test:
        exit(testOpennic())

    if args.undo:
        exit(undo(DIR_RESOLVCONF))
    else:
        exit(main(sys.argv[1:]))
