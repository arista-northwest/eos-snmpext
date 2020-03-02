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
    "CoppSystemLldp": 19,
    "CoppSystemMirroring": 20,
    "CoppSystemMlag": 21,
    "CoppSystemMplsArpSuppress": 22,
    "CoppSystemMplsLabelMiss": 23,
    "CoppSystemMplsTtl": 24,
    "CoppSystemMvrp": 25,
    "CoppSystemOspfIsisUcast": 26,
    "CoppSystemPtp": 27,
    "CoppSystemSflow": 28,
    "CoppSystemDefault": 29,
    "CoppSystemCfmSnoop": 30,
    "CoppSystemIpMcast": 31,
    "CoppSystemIpMcastMiss": 32,
    "CoppSystemL2Bcast": 33,
    "CoppSystemL3Ttl1IpOptions": 34,
    "CoppSystemLinkLocal": 35,
    "CoppSystemMulticastSnoop": 36,
    "CoppSystemOspfIsis": 37,
    "CoppSystemPtpSnoop": 38,
    "CoppSystemVxlanEncap": 39,
    "CoppSystemVxlanVtepLearn": 40
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