# -*- coding: utf-8 -*-

# Copyright (c) 2020 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import json
import re
import os
from six import iteritems
from eos_snmpext.util import cli, is_platform_sand, is_mock_mode

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
    |       | Index: CoppClassId
    |       |
    |       +-- String coppClass(1)
    |       |
    |       +-- Counter64 enqueuedPackets(2)
    |       |
    |       +-- Counter64 enqueuedBytes(3)
    |       |
    |       +-- Counter64 droppedPackets(4)
    |       |
    |       +-- Counter64 droppedBytes(5)

"""

MOCK_DATA = '{"egressQueues":{"sources":{"all":{"cpuPorts":{"CpuTm3":{"mcastQueues":{"queues":{"0":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"ucastQueues":{"queues":{"0":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}}},"CpuTm2":{"mcastQueues":{"queues":{"0":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"ucastQueues":{"queues":{"0":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}}},"CpuTm1":{"mcastQueues":{"queues":{"0":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"ucastQueues":{"queues":{"0":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}}},"CpuTm0":{"mcastQueues":{"queues":{"0":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"ucastQueues":{"queues":{"0":{"droppedBytes":0,"enqueuedPackets":386343,"enqueuedBytes":48264952,"droppedPackets":0}}}},"CpuTm5":{"mcastQueues":{"queues":{"0":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"ucastQueues":{"queues":{"0":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}}},"CpuTm4":{"mcastQueues":{"queues":{"0":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"ucastQueues":{"queues":{"0":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}}}}}}},"ingressVoqs":{"sources":{"all":{"cpuClasses":{"CoppSystemMirroring":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":6758,"enqueuedBytes":1491318,"droppedPackets":0}}},"CoppSystemMvrp":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemAclLog":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemDot1xMba":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemCfmSnoop":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemLinkLocal":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":89,"enqueuedBytes":8010,"droppedPackets":0}}},"CoppSystemL3LpmOverflow":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":270,"enqueuedBytes":23100,"droppedPackets":0}}},"CoppSystemDefault":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemVxlanEncap":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemLdp":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemSflow":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":34,"enqueuedBytes":4009,"droppedPackets":0}}},"CoppSystemPtpSnoop":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemRsvp":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemL3Ttl1IpOptions":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":229,"enqueuedBytes":31386,"droppedPackets":0}}},"CoppSystemIpMcast":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemMlag":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemL2Ucast":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":193,"enqueuedBytes":12380,"droppedPackets":0}}},"CoppSystemL3Ttl1IpOptUcast":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":70196,"enqueuedBytes":6878668,"droppedPackets":0}}},"CoppSystemMplsTtl":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemMplsLabelMiss":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemCvx":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemOspfIsis":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemL2Bcast":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":1083,"enqueuedBytes":69312,"droppedPackets":0}}},"CoppSystemLacp":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":50277,"enqueuedBytes":6435456,"droppedPackets":0}}},"CoppSystemIpBcast":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemIpMcastMiss":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemMplsArpSuppress":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemBgp":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":68114,"enqueuedBytes":5312892,"droppedPackets":0}}},"CoppSystemVxlanVtepLearn":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemOspfIsisUcast":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemMulticastSnoop":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemL3DstMiss":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemPtp":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemLldp":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":63600,"enqueuedBytes":12561111,"droppedPackets":0}}},"CoppSystemIgmp":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemEgressTrap":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemCvxHeartbeat":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemArpInspect":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemCfm":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemIpUcast":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemBfd":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":0,"enqueuedBytes":0,"droppedPackets":0}}},"CoppSystemBpdu":{"ports":{"":{"droppedBytes":0,"enqueuedPackets":125500,"enqueuedBytes":15436500,"droppedPackets":0}}}}}}}}'

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
    if is_mock_mode():
        return True
    
    return is_platform_sand()

def update(pp):
    
    data = None
    if is_mock_mode():
        data = json.loads(MOCK_DATA)
    else:
        data = json.loads(cli("show cpu counters queue summary | json"))

    ports = data["egressQueues"]["sources"]["all"]["cpuPorts"]
    classes = data["ingressVoqs"]["sources"]["all"]["cpuClasses"]

    for port, qtypes in iteritems(ports):
        port_id = int(re.match(r"CpuTm(\d+)", port).group(1))

        for qtype, queues in iteritems(qtypes):
            dest_type_id = QUEUE_TYPES_MAP.get(qtype)

            if dest_type_id is None:
                continue

            for queue_id, counters in iteritems(queues["queues"]):
                queue_id = int(queue_id)
                base_oid = "%d.1.1" % ROOT_OID
                idx = "%d.%d.%d" % (port_id, dest_type_id, queue_id)

                pp.add_str("%s.1.%s" % (base_oid, idx), port)
                pp.add_str("%s.2.%s" % (base_oid, idx), qtype)
                pp.add_int("%s.3.%s" % (base_oid, idx), queue_id)
                pp.add_cnt_64bit("%s.4.%s" % (base_oid, idx), counters["enqueuedPackets"])
                pp.add_cnt_64bit("%s.5.%s" % (base_oid, idx), counters["enqueuedBytes"])
                pp.add_cnt_64bit("%s.6.%s" % (base_oid, idx), counters["droppedPackets"])
                pp.add_cnt_64bit("%s.7.%s" % (base_oid, idx), counters["droppedBytes"])
        
    for copp_class, counters in iteritems(classes):
        counters = counters["ports"][""]
        copp_class_id = COPP_CLASS_MAP[copp_class]

        base_oid = "%d.2.1" % ROOT_OID

        pp.add_str("%s.1.%s" % (base_oid, copp_class_id), copp_class)
        pp.add_cnt_64bit("%s.2.%s" % (base_oid, copp_class_id), counters["enqueuedPackets"])
        pp.add_cnt_64bit("%s.3.%s" % (base_oid, copp_class_id), counters["enqueuedBytes"])
        pp.add_cnt_64bit("%s.4.%s" % (base_oid, copp_class_id), counters["droppedPackets"])
        pp.add_cnt_64bit("%s.5.%s" % (base_oid, copp_class_id), counters["droppedBytes"])
