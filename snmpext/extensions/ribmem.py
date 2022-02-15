# -*- coding: utf-8 -*-
# Copyright (c) 2021 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import glob
import os
import re
import time

"""
+--- RibMemory (12)
    |
    + --- RibMemoryTable[1]
         |
         + --- RibMemoryEntry[1]
              | Index: Hash(Name)
              |
              + String name(1)
              |
              + String timestamp[2]
              |
              + Integer pid(3)
              |
              + Integer size(4)
"""

POLLING_INTERVAL = 10
BASE_OID = ".1.3.6.1.4.1.8072.1.3.1.5.12"

def get_rib_statm(name=None):
    stats = []

    procs = glob.glob('/proc/[0-9]*')

    for path in procs:
        stat = ""
        pid = os.path.split(path)[-1]
        pid = int(pid)

        try:
            with open(os.path.join(path, "stat"), "r") as fhl:
                timestamp = time.time()
                stat = fhl.read().strip().split(' ')
        except IOError:
            # process went away before we could read it.
            continue

        #size, rss = [int(i) for i in stat.split(" ")[:2]]
        name = re.sub(r'[\(\)]', '', stat[1])
        
        if not name.startswith("Rib"):
            continue

        size = stat[22]
        
        stats.append({
            'name': name,
            'pid': pid,
            'timestamp': timestamp,
            'size': size
        })

    return stats

def update(pp=None):
    stats = get_rib_statm()
    
    base_oid = "1.1"

    for entry in stats:
        idx = abs(hash(entry["name"])) % (10 ** 8)
        pp.add_str("%s.1.%s" % (base_oid, idx), entry["name"])
        pp.add_int("%s.2.%s" % (base_oid, idx), int(entry["timestamp"]))
        pp.add_int("%s.3.%s" % (base_oid, idx), entry["pid"])
        pp.add_int("%s.4.%s" % (base_oid, idx), entry["size"])
