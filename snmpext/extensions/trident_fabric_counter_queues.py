# -*- coding: utf-8 -*-

from six import iteritems
import json
import re

from eos_snmpext.util import cli, platform, version

"""
|  +--fabricQueueTable(1)
|  |  |
|  |  +--fabricQueueEntry(1)
|  |     |  Index: moduleId, interfaceId, queueId
|  |     |
|  |     +-- String fabricQueueModule(1)
|  |     |
|  |     +-- String fabricQueuePort(2)
|  |     |
|  |     +-- String fabricQueueTxQ(3)
|  |     |
|  |     +-- Counter64 fabricEnqueuedPackets(4)
|  |     |
|  |     +-- Counter64 fabricEnqueuedBytes(5)
|  |     |
|  |     +-- Counter64 fabricQueueDroppedBytes(6)
|  |     |
|  |     +-- Counter64 fabricDroppedPackets(7)
|  |
|  +--fabricQueueSummary(2)
|  |  |
|  |  +-- Counter64 fabricQueueEnqueuedPackets(1)
|  |  |
|  |  +-- Counter64 fabricQueueEnqueuedBytes(2)
|  |  |
|  |  +-- Counter64 fabricQueueDroppedBytes(3)
|  |  |
|  |  +-- Counter64 fabricQueueDroppedPackets(4)
"""

# Map queue names to an OID
queue_map = {
    "UC0": "1.0",
    "UC1": "1.1",
    "UC2": "1.2",
    "UC3": "1.3",
    "UC4": "1.4",
    "UC5": "1.5",
    "UC6": "1.6",
    "UC7": "1.7",
    "UC8": "1.8",
    "MC0": "2.0",
    "MC1": "2.1",
    "MC2": "2.2",
    "MC3": "2.3",
    "MC4": "2.4",
    "MC5": "2.5",
    "MC6": "2.6",
    "MC7": "2.7",
    "MC8": "2.8"
}

field_map = {
    "enqueuedPackets": 4, 
    "enqueuedBytes": 5,
    "droppedBytes": 6,
    "droppedPackets": 7
}

BASE_OID = ".1.3.6.1.4.1.8072.1.3.1.5.10"
POLLING_INTERVAL = 30

def supported():
    ver = version()
    return ver["modelName"].startswith("DCS-7260CX")

def update(pp):
    # with open("trident_fabric_counter_queues.json") as fh:
    #     data = json.loads(fh.read())
    response = cli("show platform trident fabric counter queue detail | json")
    data = json.loads(response)
    
    summary = {k: 0 for (k, v) in iteritems(field_map)}

    for fabric, ports_ in iteritems(data["fabricChips"]):
        # print(fabric)
        ports = ports_["ports"]
        module_id = ports_["modId"]
        
        for port, queues in iteritems(ports):
            
            # build an integer port ID
            port_id = ".".join(re.findall(r"(\d+)", port))
            

            for dqueue, fields in iteritems(queues["destinationQueues"]):
                dqueue_id = queue_map[dqueue]
                #field_id = field_map

                oid = "1.1.%d.%s.%s" % (module_id, port_id, dqueue_id)

                #print("%s %s %s %d.%s.%s" % (fabric, port, dqueue, module_id, port_id, dqueue_id))
                
                pp.add_str("%s.1" % oid, fabric)
                pp.add_str("%s.2" % oid, port)
                pp.add_str("%s.3" % oid, dqueue)
                
                for field, value in iteritems(fields):
                    field_id = field_map[field]
                    summary[field] += value
                    pp.add_cnt_64bit("%s.%d" % (oid, field_id), value)

    pp.add_cnt_64bit("%d.2.1" % ROOT_OID, summary["enqueuedPackets"])
    pp.add_cnt_64bit("%d.2.2" % ROOT_OID, summary["enqueuedBytes"])
    pp.add_cnt_64bit("%d.2.3" % ROOT_OID, summary["droppedBytes"])
    pp.add_cnt_64bit("%d.2.4" % ROOT_OID, summary["droppedPackets"])
