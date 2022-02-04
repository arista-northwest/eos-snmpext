# -*- coding: utf-8 -*-
"""
+--- ipsecConnections
    |
    +--- ipsecConnectionsTable
        |
        +--- ipsecConnectionsEntry
            | Index: sAddr, dAddr
            |
            +-- String ipsecConnectionName(1)
            |
            +-- String ipsecConnectionTunnelIf(2)
            |
            +-- String ipsecConnectionTunnelState(2)
            |
            +-- String ipsecConnectionUpTime(2)
            |
            +-- String ipsecConnectionSourceAddr(3)
            |
            +-- String ipsecConnectionDestAddr(4)
            |
            +-- String ipsecConnectionTunnelNs(5)
            |
            +-- Integer ipsecConnectionRekeyTime(6)
            |
            +-- Counter64 ipsecConnectionInputDataBytes(7)
            |
            +-- Counter64 ipsecConnectionOutputDataPkts(8)
            |
            +-- Counter64 ipsecConnectionInputDataPkts(9)
            |
            +-- Counter64 ipsecConnectionOutputDataBytes(10)
"""

from __future__ import print_function

import json
from snmpext.util import is_mock_mode, cli

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
POLLING_INTERVAL = 10

def update(pp):
    data = None
    if is_mock_mode():
        data = json.loads(MOCK_DATA)
    else:
        data = json.loads(cli("show ip security connection | json"))

    base_oid = "%s.1.1" % ROOT_OID
    
    for _, elem in data["connections"].items():
        idx = ".".join([elem["saddr"], elem["daddr"]])

        if len(elem["tunnelDict"]) < 1:
            return

        tunnel_intf, tunnel_state = elem["tunnelDict"].items()[0]
            
        pp.add_str("%s.1.%s" % (base_oid, idx), elem["connName"])
        pp.add_str("%s.2.%s" % (base_oid, idx), tunnel_intf)
        pp.add_str("%s.3.%s" % (base_oid, idx), tunnel_state)
        pp.add_str("%s.4.%s" % (base_oid, idx), elem["upTimeStr"])
        pp.add_str("%s.5.%s" % (base_oid, idx), elem["saddr"])
        pp.add_str("%s.6.%s" % (base_oid, idx), elem["daddr"])
        pp.add_str("%s.7.%s" % (base_oid, idx), elem["tunnelNs"])
        pp.add_int("%s.8.%s" % (base_oid, idx), elem["rekeyTime"])
        pp.add_cnt_64bit("%s.9.%s" % (base_oid, idx), elem["ipsecInputDataBytes"])
        pp.add_cnt_64bit("%s.10.%s" % (base_oid, idx), elem["ipsecOutputDataPkts"])
        pp.add_cnt_64bit("%s.11.%s" % (base_oid, idx), elem["ipsecInputDataPkts"])
        pp.add_cnt_64bit("%s.12.%s" % (base_oid, idx), elem["ipsecOutputDataBytes"])