EOS SNMP extensions
===================

Installation
------------

Download

https://github.com/arista-northwest/eos_snmpext/releases

Or... build the RPM (rpm tools required)

```bash
git clone https://github.com/arista-northwest/eos_snmpext.git
cd eos_snmpext
python setup.py bdist_rpm
```

Installation

```
scp dist/eos_snmpext-0.1.13-1.noarch.rpm <username>@<switch>:/tmp/

ssh <username>@<switch>

! clean up the old version, if it exists
no extension eos_snmpext-0.1.13-1.noarch.rpm
delete extension:eos_snmpext-0.1.13-1.noarch.rpm

copy file:/tmp/eos_snmpext-0.1.13-1.noarch.rpm extension:
extension eos_snmpext-0.1.13-1.noarch.rpm

! make persistent
copy installed-extensions boot-extensions

! restart the extension
configure
no snmp-server extension .1.3.6.1.4.1.8072.1.3.1.5
snmp-server extension .1.3.6.1.4.1.8072.1.3.1.5 file:/var/tmp/snmpext
end
```

If this is a Trident2 switch...

Map of trident2_l3_summary:

```
+---Trident2L3Stats(1)
    |
    +--- -R-- Gauge  nextHopEntriesUsed(1)  (integer)
    +--- -R-- Gauge  nextHopEntriesSize(2)  (integer)
    +--- -R-- Gauge  hostTableMode(3)       (integer)
    +--- -R-- Gauge  hostTableUsed(4)       (integer)
    +--- -R-- Gauge  hostTableSize(5)       (integer)
    +--- -R-- Gauge  lpmTableMode(6)        (integer)
    +--- -R-- Gauge  lpmTableUsed(7)        (integer)
    +--- -R-- Gauge  lpmTableSize(8)        (integer)
    +--- -R-- Gauge  ipv4Entries(9)         (integer)
    +--- -R-- Gauge  ipv4Routes(10)         (integer)
    +--- -R-- Gauge  ipv6Entries(11)        (integer)
    +--- -R-- Gauge  ipv6Routes(12)         (integer)
    +--- -R-- Gauge  alpmTableMode(13)      (integer)
    +--- -R-- Gauge  alpmTableUsed(14)      (integer)
    +--- -R-- Gauge  alpmTableSize(15)      (integer)
```

```bash
switch#show snmp mib walk .1.3.6.1.4.1.8072.1.3.1.5.1
NET-SNMP-EXTEND-MIB::netSnmpExtendMIB.5.1.1 = Gauge32: 43
NET-SNMP-EXTEND-MIB::netSnmpExtendMIB.5.1.2 = Gauge32: 49151
NET-SNMP-EXTEND-MIB::netSnmpExtendMIB.5.1.3 = Gauge32: 4
NET-SNMP-EXTEND-MIB::netSnmpExtendMIB.5.1.4 = Gauge32: 31
NET-SNMP-EXTEND-MIB::netSnmpExtendMIB.5.1.5 = Gauge32: 16383
NET-SNMP-EXTEND-MIB::netSnmpExtendMIB.5.1.6 = Gauge32: 4
NET-SNMP-EXTEND-MIB::netSnmpExtendMIB.5.1.7 = Gauge32: 12
NET-SNMP-EXTEND-MIB::netSnmpExtendMIB.5.1.8 = Gauge32: 393216
NET-SNMP-EXTEND-MIB::netSnmpExtendMIB.5.1.9 = Gauge32: 1
NET-SNMP-EXTEND-MIB::netSnmpExtendMIB.5.1.10 = Gauge32: 2
NET-SNMP-EXTEND-MIB::netSnmpExtendMIB.5.1.11 = Gauge32: 3
NET-SNMP-EXTEND-MIB::netSnmpExtendMIB.5.1.12 = Gauge32: 2
NET-SNMP-EXTEND-MIB::netSnmpExtendMIB.5.1.13 = Gauge32: 4
NET-SNMP-EXTEND-MIB::netSnmpExtendMIB.5.1.14 = Gauge32: 12
NET-SNMP-EXTEND-MIB::netSnmpExtendMIB.5.1.15 = Gauge32: 393216
```

Usage
-----

For testing/debugging

Note: extensions need to be explicitly enabled in the config file (/mnt/flash/snmpext-config)

```bash
[admin@switch ~]$ cat /mnt/flash/snmpext-config
extensions:
    - hello

[admin@switch ~]$ snmpext
PING
PONG
get
.1.3.6.1.4.1.8072.1.3.1.5.255.0
.1.3.6.1.4.1.8072.1.3.1.5.255.0
STRING
Hello World!
```

Extending (optional)
--------------------

Simplest example, with polling interval set

```python
# -*- coding: utf-8 -*-

POLLING_INTERVAL = 5

def update(pp):
    pp.add_str('255.0', 'Hello World!')

```

Make sure the 'snmpext' python package exists on the switch:

```
switch# mkdir flash:/snmpext
switch# bash touch /mnt/flash/snmpext/__init__.py
```

From a workstation:

```bash
$ scp myextension.py user@switch:/mnt/flash/snmpext/myextension.py
```

Restart the SNMP agent:


Test a new extension:

```bash
[admin@switch ~]$ snmpext -d myextension
```
