# -*- coding: utf-8 -*-

# Copyright (c) 2023 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

from snmpext import PassPersist
import json
import re

from typing import Dict
from snmpext.util import cli, cli_json


cq = """{
    "ingressVoqCounters": {
        "interfaces": {
            "Ethernet23/1": {
                "trafficClasses": {
                    "TC6": {
                        "droppedBytes": 0,
                        "enqueuedPackets": 0,
                        "enqueuedBytes": 0,
                        "droppedPackets": 0
                    },
                    "TC7": {
                        "droppedBytes": 0,
                        "enqueuedPackets": 0,
                        "enqueuedBytes": 0,
                        "droppedPackets": 0
                    },
                    "TC4": {
                        "droppedBytes": 0,
                        "enqueuedPackets": 0,
                        "enqueuedBytes": 0,
                        "droppedPackets": 0
                    },
                    "TC5": {
                        "droppedBytes": 0,
                        "enqueuedPackets": 0,
                        "enqueuedBytes": 0,
                        "droppedPackets": 0
                    },
                    "TC2": {
                        "droppedBytes": 0,
                        "enqueuedPackets": 0,
                        "enqueuedBytes": 0,
                        "droppedPackets": 0
                    },
                    "TC3": {
                        "droppedBytes": 0,
                        "enqueuedPackets": 0,
                        "enqueuedBytes": 0,
                        "droppedPackets": 0
                    },
                    "TC0": {
                        "droppedBytes": 2342432324,
                        "enqueuedPackets": 1231231,
                        "enqueuedBytes": 678678,
                        "droppedPackets": 345343
                    },
                    "TC1": {
                        "droppedBytes": 0,
                        "enqueuedPackets": 0,
                        "enqueuedBytes": 0,
                        "droppedPackets": 0
                    }
                }
            }
        }
    }
}
"""

BASE_OID = ".1.3.6.1.4.1.8072.1.3.1.5.10"
POLLING_INTERVAL = 60

indexes = """RWA-sdm203#show snmp mib walk ifdescr
IF-MIB::ifDescr[1001] = STRING: Ethernet23/1
IF-MIB::ifDescr[999001] = STRING: Management1
IF-MIB::ifDescr[5000000] = STRING: Loopback0
IF-MIB::ifDescr[5000001] = STRING: Loopback1
IF-MIB::ifDescr[7000001] = STRING: Vxlan1
IF-MIB::ifDescr[1152639077] = STRING: Port-Channel101.300
"""
def get_ifindexes() -> Dict[str, int]:
    map: Dict[str, int] = {}
    rsp = cli("show snmp mib walk ifdescr")
    #rsp = indexes
    for line in rsp.splitlines():
        line = line.strip()
        match = re.search(r"IF-MIB::ifDescr\[(\d+)\] = STRING\: (.*)$", line)
        if match:
            ifindex, descr = match.groups()
            map[descr] = int(ifindex)

    return map

            


def update(pp: PassPersist):
    response = cli_json("show interfaces counters queue")
    indexes = get_ifindexes()
    #response = json.loads(cq)
    for interface, tcs in response['ingressVoqCounters']['interfaces'].items():
        idx = indexes[interface]
        for tc, counters in tcs['trafficClasses'].items():
            i = re.match("TC(\d+)", tc).group(1)
            pp.add_cnt_64bit("{}.1.{}.{}".format(BASE_OID, idx, i), counters['enqueuedPackets'])
            pp.add_cnt_64bit("{}.1.{}.{}".format(BASE_OID, idx, i), counters['enqueuedBytes'])
            pp.add_cnt_64bit("{}.1.{}.{}".format(BASE_OID, idx, i), counters['droppedPackets'])
            pp.add_cnt_64bit("{}.1.{}.{}".format(BASE_OID, idx, i), counters['droppedBytes'])


if __name__ == "__main__":
    PassPersist(BASE_OID).run(update, POLLING_INTERVAL)