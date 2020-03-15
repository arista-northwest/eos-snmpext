# -*- coding: utf-8 -*-

# Copyright (c) 2020 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import json
import re
from six import iteritems
from eos_snmpext.util import cli, is_platform_sand

"""
+--- cpuCountersQueue (11)
    |
    +--- egressQueuesSummaryTable(1)
    |   |
    |   +--- egressQueuesSummaryEntry(1)
    |       | Index: portId, destTypeId, queueId
    |       |
    |       +-- String port(1)
    |       |
    |       +-- String destType(2)
    |       |
    |       +-- Integer queue(3)
    |       |
    |       +-- Counter64 enqueuedPackets(4)
    |       |
    |       +-- Counter64 enqueuedBytes(5)
    |       |
    |       +-- Counter64 droppedPackets(6)
    |       |
    |       +-- Counter64 droppedBytes(7)
    |
    +--- ingressVoqsSummaryTable(2)
    |   |
    |   +--- ingressVoqsSummaryEntry(1)
    |       | Index: CoppClassPriority
    |       |
    |       +-- String coppClass(1)
    |       |
    |       +-- Integer coppClassPriority(2)
    |       |
    |       +-- Counter64 enqueuedPackets(3)
    |       |
    |       +-- Counter64 enqueuedBytes(4)
    |       |
    |       +-- Counter64 droppedPackets(5)
    |       |
    |       +-- Counter64 droppedBytes(6)

"""

ROOT_OID = 11
POLLING_INTERVAL = 10

COPP_CLASS_MAP = {
    "CoppSystemAclLog": 1,
    "CoppSystemArpInspect": 2,
    "CoppSystemBfd": 3,
    "CoppSystemBgp": 4,
    "CoppSystemBpdu": 5,
    "CoppSystemCfm": 6,
    "CoppSystemCvx": 7,
    "CoppSystemCvxHeartbeat": 8,
    "CoppSystemDot1xMba": 9,
    "CoppSystemEgressTrap": 10,
    "CoppSystemIgmp": 11,
    "CoppSystemIpBcast": 12,
    "CoppSystemIpUcast": 13,
    "CoppSystemL2Ucast": 14,
    "CoppSystemL3DstMiss": 15,
    "CoppSystemL3LpmOverflow": 16,
    "CoppSystemL3Ttl1IpOptUcast": 17,
    "CoppSystemLacp": 18,
    "CoppSystemLdp": 19,
    "CoppSystemLldp": 20,
    "CoppSystemMirroring": 21,
    "CoppSystemMlag": 22,
    "CoppSystemMplsArpSuppress": 23,
    "CoppSystemMplsLabelMiss": 24,
    "CoppSystemMplsTtl": 25,
    "CoppSystemMvrp": 26,
    "CoppSystemOspfIsisUcast": 27,
    "CoppSystemPtp": 28,
    "CoppSystemRsvp": 29,
    "CoppSystemSflow": 30,
    "CoppSystemDefault": 31,
    "CoppSystemCfmSnoop": 32,
    "CoppSystemIpMcast": 33,
    "CoppSystemIpMcastMiss": 34,
    "CoppSystemL2Bcast": 35,
    "CoppSystemL3Ttl1IpOptions": 36,
    "CoppSystemLinkLocal": 37,
    "CoppSystemMulticastSnoop": 38,
    "CoppSystemOspfIsis": 39,
    "CoppSystemPtpSnoop": 40,
    "CoppSystemVxlanEncap": 41,
    "CoppSystemVxlanVtepLearn": 42 
}

QUEUE_TYPES_MAP = {
    "ucastQueues": 0,
    "mcastQueues": 1
}

def supported():
    return is_platform_sand()

def update(pp):
    data = json.loads(cli("show cpu counters queue summary | json"))
    ports = data["egressQueues"]["sources"]["all"]["cpuPorts"]
    classes = data["ingressVoqs"]["sources"]["all"]["cpuClasses"]

    for port, qtypes in iteritems(ports):
        
        port_id = int(re.match(r"CpuTm(\d+)", port).group(1))

        for qtype, queues in iteritems(qtypes):
            dest_type_id = QUEUE_TYPES_MAP.get(qtype)

            if not dest_type_id:
                continue

            for queue_id, counters in iteritems(queues["queues"]):
                queue_id = int(queue_id)
                oid = "%d.1.1.%d.%d.%d" % (ROOT_OID, port_id, dest_type_id, queue_id)

                pp.add_str("%s.1" % oid, port)
                pp.add_cnt_64bit("%s.2" % oid, counters["enqueuedPackets"])
                pp.add_cnt_64bit("%s.3" % oid, counters["enqueuedBytes"])
                pp.add_cnt_64bit("%s.4" % oid, counters["droppedPackets"])
                pp.add_cnt_64bit("%s.5" % oid, counters["droppedBytes"])
        
    for copp_class, counters in iteritems(classes):
        counters = counters["ports"][""]
        copp_class_id = COPP_CLASS_MAP[copp_class]
        oid = "%d.2.1.%d" % (ROOT_OID, copp_class_id)

        pp.add_str("%s.1" % oid, copp_class)
        pp.add_cnt_64bit("%s.2" % oid, counters["enqueuedPackets"])
        pp.add_cnt_64bit("%s.3" % oid, counters["enqueuedBytes"])
        pp.add_cnt_64bit("%s.4" % oid, counters["droppedPackets"])
        pp.add_cnt_64bit("%s.5" % oid, counters["droppedBytes"])

if __name__ == "__main__":
    update(None)