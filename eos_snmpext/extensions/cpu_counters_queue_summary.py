# -*- coding: utf-8 -*-

# Copyright (c) 2020 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import json
import re
from six import iteritems
from eos_snmpext.util import cli, platform, memoize, is_platform_sand

DATA = """{
    "egressQueues": {
        "sources": {
            "all": {
                "cpuPorts": {
                    "CpuTm3": {
                        "mcastQueues": {
                            "queues": {
                                "0": {
                                    "droppedBytes": 0,
                                    "enqueuedPackets": 0,
                                    "enqueuedBytes": 0,
                                    "droppedPackets": 0
                                }
                            }
                        },
                        "ucastQueues": {
                            "queues": {
                                "0": {
                                    "droppedBytes": 0,
                                    "enqueuedPackets": 0,
                                    "enqueuedBytes": 0,
                                    "droppedPackets": 0
                                }
                            }
                        }
                    },
                    "CpuTm2": {
                        "mcastQueues": {
                            "queues": {
                                "0": {
                                    "droppedBytes": 0,
                                    "enqueuedPackets": 0,
                                    "enqueuedBytes": 0,
                                    "droppedPackets": 0
                                }
                            }
                        },
                        "ucastQueues": {
                            "queues": {
                                "0": {
                                    "droppedBytes": 0,
                                    "enqueuedPackets": 0,
                                    "enqueuedBytes": 0,
                                    "droppedPackets": 0
                                }
                            }
                        }
                    },
                    "CpuTm1": {
                        "mcastQueues": {
                            "queues": {
                                "0": {
                                    "droppedBytes": 0,
                                    "enqueuedPackets": 0,
                                    "enqueuedBytes": 0,
                                    "droppedPackets": 0
                                }
                            }
                        },
                        "ucastQueues": {
                            "queues": {
                                "0": {
                                    "droppedBytes": 0,
                                    "enqueuedPackets": 0,
                                    "enqueuedBytes": 0,
                                    "droppedPackets": 0
                                }
                            }
                        }
                    },
                    "CpuTm0": {
                        "mcastQueues": {
                            "queues": {
                                "0": {
                                    "droppedBytes": 0,
                                    "enqueuedPackets": 393491,
                                    "enqueuedBytes": 1647046989,
                                    "droppedPackets": 0
                                }
                            }
                        },
                        "ucastQueues": {
                            "queues": {
                                "0": {
                                    "droppedBytes": 0,
                                    "enqueuedPackets": 26374239,
                                    "enqueuedBytes": 140211258135,
                                    "droppedPackets": 0
                                }
                            }
                        }
                    },
                    "CpuTm5": {
                        "mcastQueues": {
                            "queues": {
                                "0": {
                                    "droppedBytes": 0,
                                    "enqueuedPackets": 0,
                                    "enqueuedBytes": 0,
                                    "droppedPackets": 0
                                }
                            }
                        },
                        "ucastQueues": {
                            "queues": {
                                "0": {
                                    "droppedBytes": 0,
                                    "enqueuedPackets": 0,
                                    "enqueuedBytes": 0,
                                    "droppedPackets": 0
                                }
                            }
                        }
                    },
                    "CpuTm4": {
                        "mcastQueues": {
                            "queues": {
                                "0": {
                                    "droppedBytes": 0,
                                    "enqueuedPackets": 0,
                                    "enqueuedBytes": 0,
                                    "droppedPackets": 0
                                }
                            }
                        },
                        "ucastQueues": {
                            "queues": {
                                "0": {
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
        }
    },
    "ingressVoqs": {
        "sources": {
            "all": {
                "cpuClasses": {
                    "CoppSystemMirroring": {
                        "ports": {
                            "": {
                                "droppedBytes": 2553342499254,
                                "enqueuedPackets": 24393382,
                                "enqueuedBytes": 137957158560,
                                "droppedPackets": 318898833
                            }
                        }
                    },
                    "CoppSystemMvrp": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemAclLog": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemDot1xMba": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemCfmSnoop": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemLinkLocal": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 172668,
                                "enqueuedBytes": 15216510,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemL3LpmOverflow": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 22340,
                                "enqueuedBytes": 1742520,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemDefault": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemVxlanEncap": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemSflow": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 510065,
                                "enqueuedBytes": 2162736871,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemPtpSnoop": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemMulticastSnoop": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemL3Ttl1IpOptions": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemIpMcast": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemMlag": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemL2Ucast": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 192,
                                "enqueuedBytes": 12288,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemL3Ttl1IpOptUcast": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemMplsTtl": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemMplsLabelMiss": {
                        "ports": {
                            "": {
                                "droppedBytes": 3177588,
                                "enqueuedPackets": 64,
                                "enqueuedBytes": 512256,
                                "droppedPackets": 397
                            }
                        }
                    },
                    "CoppSystemCvx": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemOspfIsis": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 232518,
                                "enqueuedBytes": 1535309202,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemL2Bcast": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 38,
                                "enqueuedBytes": 2692,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemLacp": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 1284087,
                                "enqueuedBytes": 153781232,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemIpBcast": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemIpMcastMiss": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemMplsArpSuppress": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemBgp": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 64228,
                                "enqueuedBytes": 5173965,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemVxlanVtepLearn": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemOspfIsisUcast": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemL3DstMiss": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 5,
                                "enqueuedBytes": 705,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemPtp": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemLldp": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 63365,
                                "enqueuedBytes": 14371893,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemIgmp": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemEgressTrap": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 1069,
                                "enqueuedBytes": 9778764,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemCvxHeartbeat": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemArpInspect": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemCfm": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemIpUcast": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 23709,
                                "enqueuedBytes": 2131826,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemBfd": {
                        "ports": {
                            "": {
                                "droppedBytes": 0,
                                "enqueuedPackets": 0,
                                "enqueuedBytes": 0,
                                "droppedPackets": 0
                            }
                        }
                    },
                    "CoppSystemBpdu": {
                        "ports": {
                            "": {
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
    }
}"""

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
            dest_type_id = QUEUE_TYPES_MAP[qtype]

            for queue_id, counters in iteritems(queues["queues"]):
                queue_id = int(queue_id)
                oid = "%d.1.1.%d.%d.%d" % (ROOT_OID, port_id, dest_type_id, queue_id)

                #print("%s.1" % oid, port)
                pp.add_str("%s.1" % oid, port)
                
                #print("%s.2" % oid, counters["enqueuedPackets"])
                pp.add_cnt_64bit("%s.2" % oid, counters["enqueuedPackets"])
                
                #print("%s.3" % oid, counters["enqueuedBytes"])
                pp.add_cnt_64bit("%s.3" % oid, counters["enqueuedBytes"])

                #print("%s.4" % oid, counters["droppedPackets"])
                pp.add_cnt_64bit("%s.4" % oid, counters["droppedPackets"])

                #print("%s.5" % oid, counters["droppedBytes"])
                pp.add_cnt_64bit("%s.5" % oid, counters["droppedBytes"])
        
    for copp_class, counters in iteritems(classes):
        counters = counters["ports"][""]
        copp_class_id = COPP_CLASS_MAP[copp_class]
        oid = "%d.2.1.%d" % (ROOT_OID, copp_class_id)

        #print("%s.1" % oid, copp_class)
        pp.add_str("%s.1" % oid, port)
        
        #print("%s.2" % oid, counters["enqueuedPackets"])
        pp.add_cnt_64bit("%s.2" % oid, counters["enqueuedPackets"])
        
        #print("%s.3" % oid, counters["enqueuedBytes"])
        pp.add_cnt_64bit("%s.3" % oid, counters["enqueuedBytes"])

        #print("%s.4" % oid, counters["droppedPackets"])
        pp.add_cnt_64bit("%s.4" % oid, counters["droppedPackets"])

        #print("%s.5" % oid, counters["droppedBytes"])
        pp.add_cnt_64bit("%s.5" % oid, counters["droppedBytes"])

if __name__ == "__main__":
    update(None)