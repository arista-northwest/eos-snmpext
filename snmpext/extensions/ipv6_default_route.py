# -*- coding: utf-8 -*-

from __future__ import print_function
import json
from binascii import hexlify
import re
import socket
#import re
from snmpext.util import cli, platform

'''
{
    "vrfs": {
        "default": {
            "routes": {
                "::/0": {
                    "kernelProgrammed": true,
                    "directlyConnected": false,
                    "preference": 200,
                    "routeAction": "forward",
                    "vias": [
                        {
                            "interface": "Port-Channel62",
                            "nexthopAddr": "fd00:169:254::5a"
                        }
                    ],
                    "metric": 0,
                    "hardwareProgrammed": true,
                    "routeType": "bgp"
                }
            },
            "allRoutesProgrammedKernel": true,
            "routingDisabled": false,
            "allRoutesProgrammedHardware": true,
            "defaultRouteState": "reachable"
        }
    }
}
'''

'''
|  +--ipv6RouteTable(11)
   |  |  |
   |  |  +--ipv6RouteEntry(1)
   |  |     |  Index: ipv6RouteDest, ipv6RoutePfxLength, ipv6RouteIndex
   |  |     |
   |  |     +-- ---- String    ipv6RouteDest(1)
   |  |     |        Textual Convention: Ipv6Address
   |  |     |        Size: 16
   |  |     +-- ---- INTEGER   ipv6RoutePfxLength(2)
   |  |     |        Range: 0..128
   |  |     +-- ---- Unsigned  ipv6RouteIndex(3)
   |  |     +-- -R-- Integer32 ipv6RouteIfIndex(4)
   |  |     |        Textual Convention: Ipv6IfIndexOrZero
   |  |     |        Range: 0..2147483647
   |  |     +-- -R-- String    ipv6RouteNextHop(5)
   |  |     |        Textual Convention: Ipv6Address
   |  |     |        Size: 16
#    |  |     +-- -R-- EnumVal   ipv6RouteType(6)
#    |  |     |        Values: other(1), discard(2), local(3), remote(4)
#    |  |     +-- -R-- EnumVal   ipv6RouteProtocol(7)
#    |  |     |        Values: other(1), local(2), netmgmt(3), ndisc(4), rip(5), ospf(6), bgp(7), idrp(8), igrp(9)
#    |  |     +-- -R-- Integer32 ipv6RoutePolicy(8)
#    |  |     +-- -R-- Unsigned  ipv6RouteAge(9)
#    |  |     +-- -R-- Unsigned  ipv6RouteNextHopRDI(10)
#    |  |     +-- -R-- Unsigned  ipv6RouteMetric(11)
#    |  |     +-- -R-- Unsigned  ipv6RouteWeight(12)
#    |  |     +-- -R-- ObjID     ipv6RouteInfo(13)
#    |  |     |        Textual Convention: RowPointer
#    |  |     +-- -RW- EnumVal   ipv6RouteValid(14)
#    |  |              Textual Convention: TruthValue
#    |  |              Values: true(1), false(2)
'''

POLLING_INTERVAL = 60
ROOT_OID = 3

def ipv6_octet_string(addr):
    hexaddr = hexlify(socket.inet_pton(socket.AF_INET6, addr))
    lst = re.split("(\w\w)", hexaddr)[1::2]
    return list(map(lambda x: int(x, 16), lst))

def update(pp):

    response = cli("show ipv6 route ::/0 | json")
    data = json.loads(response)

    for route in data["vrfs"]["default"]["routes"]:
        vias = data["vrfs"]["default"]["routes"][route]["vias"]
        prefix, plen = route.split("/")
        octstr = ipv6_octet_string(prefix)
        
        for i in range(len(vias)):
            interface = vias[i].get("interface") or ""
            nexthop = vias[i].get("nexthopAddr") or ""
            index = ".".join(map(lambda x: str(x), octstr + [plen, i]))
            
            response = cli("show snmp mib ifmib ifindex %s | json" % interface)
            
            #print(">>" + str(response) + "<<")
            resp_ = json.loads(response)
            ifindex = resp_["ifIndex"][interface]
            pp.add_str("%d.%s.1" % (ROOT_OID, index), prefix) # ipv6RouteDest (string)
            pp.add_int("%d.%s.2" % (ROOT_OID, index), int(plen)) # ipv6RoutePfxLength (int)
            pp.add_int("%d.%s.3" % (ROOT_OID, index), i) # ipv6RouteIndex (int)
            pp.add_int("%d.%s.4" % (ROOT_OID, index), ifindex) # ipv6RouteIfIndex (int)
            pp.add_str("%d.%s.5" % (ROOT_OID, index), nexthop) # ipv6RouteNextHop
