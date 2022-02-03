# -*- coding: utf-8 -*-
"""
+--- ipsecConnections
    |
    +--- ipsecConnectionsTable
        |
        +--- ipsecConnectionsEntry
            | Index: sAddr, dAddr
            |
            +-- String connName(1)
            |
            +-- String connUpTime(2)
            |
            +-- String sAddr(3)
            |
            +-- String dAddr(4)
            |
            +-- String tunnelNs(5)
            |
            +-- Integer rekeyTime(6)
            |
            +-- Counter64 ipsecInputDataBytes(7)
            |
            +-- Counter64 ipsecOutputDataPkts(8)
            |
            +-- Counter64 ipsecInputDataPkts(9)
            |
            +-- Counter64 ipsecOutputDataBytes(10)
"""

from __future__ import print_function

import json
from eos_snmpext.util import is_mock_mode, cli

MOCK_DATA = """{
    "connections": {
        "default-1.1.1.101-1.1.1.102": {
            "tunnelDict": {
                "Tunnel1": "Established"
            },
            "upTimeStr": "12 minutes, 46 seconds",
            "pathDict": {},
            "connName": "default-1.1.1.101-1.1.1.102",
            "saddr": "1.1.1.101",
            "daddr": "1.1.1.102",
            "ipsecInputDataBytes": 51150,
            "ipsecOutputDataPkts": 780,
            "tunnelNs": "default",
            "ipsecInputDataPkts": 777,
            "ipsecOutputDataBytes": 51349,
            "rekeyTime": 1868
        }
    }
}"""

ROOT_OID = 6

def update(pp):
    data = None
    if is_mock_mode():
        data = json.loads(MOCK_DATA)
    else:
        data = json.loads(cli("show ip security connection | json"))

    base_oid = "%s.1.1" % ROOT_OID

    for _, elem in data["connections"].items():
        idx = ".".join([elem["saddr"], elem["daddr"]])
        pp.add_str("%s.1.%s" % (base_oid, idx), elem["connName"])
        pp.add_str("%s.2.%s" % (base_oid, idx), elem["upTimeStr"])
        pp.add_str("%s.3.%s" % (base_oid, idx), elem["saddr"])
        pp.add_str("%s.4.%s" % (base_oid, idx), elem["daddr"])
        pp.add_str("%s.5.%s" % (base_oid, idx), elem["tunnelNs"])
        pp.add_int("%s.6.%s" % (base_oid, idx), elem["rekeyTime"])
        pp.add_cnt_64bit("%s.7.%s" % (base_oid, idx), elem["ipsecInputDataBytes"])
        pp.add_cnt_64bit("%s.8.%s" % (base_oid, idx), elem["ipsecOutputDataPkts"])
        pp.add_cnt_64bit("%s.9.%s" % (base_oid, idx), elem["ipsecInputDataPkts"])
        pp.add_cnt_64bit("%s.10.%s" % (base_oid, idx), elem["ipsecOutputDataBytes"])