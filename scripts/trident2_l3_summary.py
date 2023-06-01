# -*- coding:utf-8 -*-

import re
from snmpext.util import cli, platform

"""

Map of platform_l3_stats MIB :

+---Trident2L3Stats(1)
    |
    +--- -R-- Gauge  nextHopEntriesUsed(1)  (integer)
    +--- -R-- Gauge  nextHopEntriesSize(2)  (integer)
    +--- -R-- Gauge  hostTableMode(3)       (integer)
    +--- -R-- Gauge  hostTableUsed(4)       (integer)
    +--- -R-- Gauge  hostTableSize(5)       (integer)
    +--- -R-- Gauge  lpmTableMode(6)        (integer)
    +--- -R-- Gauge  lpmTableUsed(7)        (integer)
    +--- -R-- Gauge  lpmTableSize(8)        (integer)
    +--- -R-- Gauge  ipv4Entries(9)         (integer)
    +--- -R-- Gauge  ipv4Routes(10)         (integer)
    +--- -R-- Gauge  ipv6Entries(11)        (integer)
    +--- -R-- Gauge  ipv6Routes(12)         (integer)
    +--- -R-- Gauge  alpmTableMode(13)      (integer)
    +--- -R-- Gauge  alpmTableUsed(14)      (integer)
    +--- -R-- Gauge  alpmTableSize(15)      (integer)
"""

POLLING_INTERVAL = 60
BASE_OID = ".1.3.6.1.4.1.8072.1.3.1.5.1"

def supported():
    return platform() == 'trident2'

def update(pp):
    response = cli("show platform trident l3 summary")

    # pre-populate ALPM with invalid entries
    data = {"alpm_table_mode": 2**32-1, "alpm_table_used": 0,
            "alpm_table_size": 0}

    for line in response.splitlines():

        # NextHop entries: 51/49151 (51 unicast, 0 multicast)
        match = re.search(r'NextHop entries: (\d+)\/(\d+)', line)
        if match:
            data["next_hop_entries_used"] = match.group(1)
            data["next_hop_entries_size"] = match.group(2)

        # Host table mode: 4, table usage: 38/16383
        match = re.search(r'Host table mode: (\d+), table usage: (\d+)\/(\d+)',
                          line)
        if match:
            data["host_table_mode"] = match.group(1)
            data["host_table_used"] = match.group(2)
            data["host_table_size"] = match.group(3)

        # LPM table mode: 2, table usage: 6/8190
        match = re.search(r'LPM table mode: (\d+), table usage: (\d+)\/(\d+)',
                          line)
        if match:
            data["lpm_table_mode"] = match.group(1)
            data["lpm_table_used"] = match.group(2)
            data["lpm_table_size"] = match.group(3)

        # IPv4 entries: 1 (full: 1, half full: 0), routes: 2
        match = re.search(r'IPv(4|6) entries: (\d+).*, routes: (\d+)', line)
        if match:
            ver = match.group(1)
            data["ipv{}_entries".format(ver)] = match.group(2)
            data["ipv{}_routes".format(ver)] = match.group(3)

        # ALPM table mode: 4, table usage: 15/393216
        match = re.search(r'ALPM table mode: (\d+), table usage: (\d+)\/(\d+)',
                          line)
        if match:
            data["alpm_table_mode"] = match.group(1)
            data["alpm_table_used"] = match.group(2)
            data["alpm_table_size"] = match.group(3)

    stats = {key: int(val) for key, val in data.items()}

    # nextHopEntriesUsed
    pp.add_gau("1", stats["next_hop_entries_used"])
    # nextHopEntriesSize
    pp.add_gau("1.2", stats["next_hop_entries_size"])
    # hostTableMode
    pp.add_gau("1.3", stats["host_table_mode"])
    # hostTableUsed
    pp.add_gau("1.4", stats["host_table_used"])
    # hostTableSize
    pp.add_gau("1.5", stats["host_table_size"])
    # lpmTableMode
    pp.add_gau("1.6", stats["lpm_table_mode"])
    # lpmTableUsed
    pp.add_gau("1.7", stats["lpm_table_used"])
    # lpmTableSize
    pp.add_gau("1.8", stats["lpm_table_size"])
    # ipv4Entries
    pp.add_gau("1.9", stats["ipv4_entries"])
    # ipv4Routes
    pp.add_gau("1.10", stats["ipv4_routes"])
    # ipv6Entries
    pp.add_gau("1.11", stats["ipv6_entries"])
    # ipv6Routes
    pp.add_gau("1.12", stats["ipv6_routes"])
    # alpmTableMode
    pp.add_gau("1.13", stats["alpm_table_mode"])
    # alpmTableUsed
    pp.add_gau("1.14", stats["alpm_table_used"])
    # alpmTableSize
    pp.add_gau("1.15", stats["alpm_table_size"])
