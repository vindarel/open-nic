#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

CONF = "/etc/dhcp3/dhclient.conf"

if not os.path.isfile(CONF):
    exit(0)

if os.path.isfile(CONF + ".back"):
    shutil.move(CONF + ".back", CONF)
