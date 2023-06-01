# -*- coding: utf-8 -*-
# Copyright (c) 2023 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

"""
show traffic-engineering rsvp tunnel
Tunnel TU.rwa01.icr01
   Source: 1.1.1.1
   Destination: 1.1.1.2
   Color: -, Metric: 11008
   State: up
   Split-tunnel: enabled
      Minimum bandwidth: 5.00 Mbps
      Maximum bandwidth: 5.00 Gbps
      Sub-tunnels limit: 20
      Sub-tunnels reduction delay: 24 hours
   Bandwidth: 5.00 Mbps, mode auto

show ip route <dest>

VRF: default
Codes: C - connected, S - static, K - kernel,
       O - OSPF, IA - OSPF inter area, E1 - OSPF external type 1,
       E2 - OSPF external type 2, N1 - OSPF NSSA external type 1,
       N2 - OSPF NSSA external type2, B - Other BGP Routes,
       B I - iBGP, B E - eBGP, R - RIP, I L1 - IS-IS level 1,
       I L2 - IS-IS level 2, O3 - OSPFv3, A B - BGP Aggregate,
       A O - OSPF Summary, NG - Nexthop Group Static Route,
       V - VXLAN Control Service, M - Martian,
       DH - DHCP client installed default route,
       DP - Dynamic Policy Route, L - VRF Leaked,
       G  - gRIBI, RC - Route Cache Route

 I L1     1.1.1.2/32 [115/11010] via 1.1.1.2/32, RSVP LER TU.rwa01.icr01 tunnel index 1
                                    via RSVP LER SUB tunnel index 1
                                       via 10.12.12.3, Port-Channel22, label imp-null(3)

+--- rsvpTeTunnels()
    |
    +--- rsvpTeTunnelsTable
        |
        +--- rsvpTeTunnelsEntry
"""

#BASE_OID = ".1.3.6.1.4.1.8072.1.3.1.5.13"