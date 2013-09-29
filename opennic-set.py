import requests
try:
    from bs4 import BeautifulSoup
except:
    print 'you need to install BeautifulSoup4: '
    print "sudo pip install BeautifulSoup4"
    exit(1)
import re
import os
import shutil

"""
Use dns servers of the open-nic project.
Fetch which are the nearest dns servers and insert them into dhclient.conf file.
"""
CONF = "/etc/dhcp3/dhclient.conf"

r = requests.get('http://www.opennicproject.org/nearest-servers/')
nic = BeautifulSoup(r.text)
assert nic
nearest = nic.find_all('div', class_='post-entry')
assert nearest[0]
dns_text = nearest[0].find('p')
assert dns_text.text
dns_list = re.findall('\d+\.\d+\.\d+\.\d+', dns_text.text)

print "nearest dns list: ", dns_list

if os.path.exists(CONF):
    shutil.copyfile(CONF, CONF + ".back")

with open(CONF, 'a') as f:
    w = "\nprepend domain-name-servers " + ", ".join(s for s in dns_list[:3]) + ";"
    print "we  add the line: " +  w + " to the file " + CONF
    print "we saved the original conf file, so if you notice any connection pb, you can still put it back"
    f.write(w)


