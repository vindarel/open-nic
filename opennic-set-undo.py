#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

CONF = "/etc/dhcp3/dhclient.conf"
BACK = "/etc/dhcp3/dhclient.conf.back"

if not os.path.isfile(CONF):
    exit(0)

if os.path.isfile(BACK):
    shutil.move(BACK, CONF)
else:
    os.remove(CONF)

