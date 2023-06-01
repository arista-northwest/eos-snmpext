# -*- coding: utf-8 -*-
# Copyright (c) 2023 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import functools
import hashlib
import json
import os
import re
import subprocess
from typing import Dict

def md5sum(*args):
    hash = hashlib.md5()
    for arg in args:
        hash.update(str(arg).encode("utf-8"))
    return hash.hexdigest()

def memoize(func):
    cache = {}
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        key = md5sum(args, kwargs)
        if key not in cache:
            cache[key] = func(*args)
        return cache[key]
    return _wrapper

def cli_json(cmd):
    rsp = cli("%s | json" % cmd)
    return json.loads(rsp)

def cli(cmd):
    cmd = "TERM=dumb Cli -p 15 -c '{}'".format(cmd)
    return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

def cli_ok(cmd):
    cmd = "TERM=dumb FastCli -p15 -c '{}' &>/dev/null; echo $?".format(cmd)
    response = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    return True if int(response) == 0 else False

# @memoize
# def is_platform_arad():
#     return cli_ok("show platform arad")
# is_arad = is_platform_arad

# @memoize
# def is_platform_sand():
#     return cli_ok("show platform sand capabilities")

# @memoize
# def is_platform_t2():
#     response = cli("show platform trident l3 summary")
#     return True if "LPM table mode:" in response else False

# @memoize
# def is_platform_tplus():
#     response = cli("show platform trident l3 summary")
#     return True if "Total lpm table entries used:" in response else False

# @memoize
# def platform():

#     platforms = {
#         'trident2': is_platform_t2,
#         'trident+': is_platform_tplus,
#         'arad': is_platform_arad
#     }

#     for name, func in platforms:
#         if func():
#             return name

@memoize
def version():
    response = cli("show version | json")
    return json.loads(response)

def is_mock_mode():
    return True if os.environ.get("SNMPEXT_MOCK_MODE", None) else False


# def memoize(f):
#     cache = {}
#     def helper(k):
#         if x not in cache:            
#             cache[k] = f(k)
#         return cache[k]
#     return helper

# @memoize
# def get_ifindex_cached(descr: str, refresh: int = 30):
#     ifindex_map = Dict[str, int]
#     rsp = cli("show snmp mib walk ifdescr")
#     for _, line in rsp:
#         match = re.search(r"IF-MIB::ifDescr\[(\d+)\] = STRING\: (.*)$", line)
#         if match:
#             idx, descr = match.groups()
#             ifindex_map[descr] = int(idx)