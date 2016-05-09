EOS SNMP extensions
===================

Installation
------------

Download

https://github.com/arista-northwest/eos_snmpext/releases/download/v0.1.0/eos_snmpext-0.1.0-1.noarch.rpm

Or... build the RPM (rpm tools required)

```bash
git clone https://github.com/arista-northwest/eos_snmpext.git
cd eos_snmpext
python setup.py bdist_rpm
```

Installation

```
scp dist/eos_snmpext-0.1.0-1.noarch.rpm <username>@<switch>:/tmp/

ssh <username>@<switch>

! clean up the old version, if it exists
no extension eos_snmpext-0.1.0-1.noarch.rpm
delete extension:eos_snmpext-0.1.0-1.noarch.rpm

copy file:/tmp/eos_snmpext-0.1.0-1.noarch.rpm extension:
extension eos_snmpext-0.1.0-1.noarch.rpm

! make persistent
copy installed-extensions boot-extensions

! restart the extension
configure
no snmp-server extension .1.3.6.1.4.1.8072.1.3.1.5
snmp-server extension .1.3.6.1.4.1.8072.1.3.1.5 file:/var/tmp/snmpext
end
```

Usage
-----

For testing/debugging

```bash
[admin@switch ~]$ snmpext -d
```

Test a new extension:

```bash
[admin@switch ~]$ snmpext -d myextension
```

Extending
---------

Simplest example, with polling interval set

```python
# -*- coding: utf-8 -*-

POLLING_INTERVAL = 5

def update(pp):
    pp.add_str('255.1', 'Hello World!')

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
