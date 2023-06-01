# -*- coding: utf-8 -*-

# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import json
from snmpext.util import cli, platform

"""
+--- SandL3Stats(2)
    |
    + ---SandL3StatsFec (1)
    |   | Index: SandL3StatsFecFeature
    |   +--- -R-- String    SandL3StatsFecFeature(1)
    |   |        Textual Convention: DisplayString
    |   |        Size: 0..255
    |   +--- -R-- Gauge     SandL3StatsFecUsed(2)
    |   +--- -R-- Gauge     SandL3StatsFecFree(3)
    |   +--- -R-- Gauge     SandL3StatsFecCommitted(4)
    |   +--- -R-- Gauge     SandL3StatsFecBestCaseMax(5)
    |   +--- -R-- Gauge     SandL3StatsFecUsedHighWatermark(6)
    |
    + ---SandL3StatsLem (2)
    |   | Index: SandL3StatsFecL3StatsLemFeature
    |   +--- -R-- String    SandL3StatsLemFeature(1)
    |   |        Textual Convention: DisplayString
    |   |        Size: 0..255
    |   +--- -R-- Gauge     SandL3StatsLemUsed(2)
    |   +--- -R-- Gauge     SandL3StatsLemFree(3)
    |   +--- -R-- Gauge     SandL3StatsLemCommitted(4)
    |   +--- -R-- Gauge     SandL3StatsLemBestCaseMax(5)
    |   +--- -R-- Gauge     SandL3StatsLemUsedHighWatermark(6)
    |
    + ---SandL3StatsRouting (3)
    |   | Index: SandL3StatsRoutingFeature
    |   +--- -R-- String    SandL3StatsRoutingFeature(1)
    |   |        Textual Convention: DisplayString
    |   |        Size: 0..255
    |   +--- -R-- Gauge     SandL3StatsRoutingUsed(2)
    |   +--- -R-- Gauge     SandL3StatsRoutingFree(3)
    |   +--- -R-- Gauge     SandL3StatsRoutingCommitted(4)
    |   +--- -R-- Gauge     SandL3StatsRoutingBestCaseMax(5)
    |   +--- -R-- Gauge     SandL3StatsRoutingUsedHighWatermark(6)
    |
    + ---SandL3StatsTcam (3)
    |   | Index: SandL3StatsTcamFeature
    |   +--- -R-- String    SandL3StatsTcamFeature(1)
    |   |        Textual Convention: DisplayString
    |   |        Size: 0..255
    |   +--- -R-- Gauge     SandL3StatsTcamUsed(2)
    |   +--- -R-- Gauge     SandL3StatsTcamFree(3)
    |   +--- -R-- Gauge     SandL3StatsTcamCommitted(4)
    |   +--- -R-- Gauge     SandL3StatsTcamBestCaseMax(5)
    |   +--- -R-- Gauge     SandL3StatsTcamUsedHighWatermark(6)
"""

ROOT_OID = 2
POLLING_INTERVAL = 60

def supported():
    return platform() == 'arad'

def update(pp):
    response = cli("show hardware capacity | json")

    data = json.loads(response)
    tables = ["FEC", "LEM", "Routing", "TCAM"]
    data = [r for r in data['tables'] if r['table'] in tables]

    for item in data:
        table = item['table']
        feature = item['feature']
        if not feature:
            if table == "LEM":
                feature = "Prefix"
            elif table == "FEC":
                feature = "Total"
            else:
                feature = "unknown"
        idx = tables.index(table) + 1
        oid = pp.encode(feature)
        #oid = re.sub('.$', '', oid)
        pp.add_str("{}.{}.1.{}".format(ROOT_OID, idx, oid), feature)
        pp.add_gau("{}.{}.2.{}".format(ROOT_OID, idx, oid), item['used'])
        pp.add_gau("{}.{}.3.{}".format(ROOT_OID, idx, oid), item['free'])
        pp.add_gau("{}.{}.4.{}".format(ROOT_OID, idx, oid), item['committed'])
        pp.add_gau("{}.{}.5.{}".format(ROOT_OID, idx, oid), item['maxLimit'])
        pp.add_gau("{}.{}.6.{}".format(ROOT_OID, idx, oid), item['highWatermark'])

    return ROOT_OID
