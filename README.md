EOS SNMP extensions
===================


Installation
------------

git clone https://github.com/arista-northwest/eos_snmpext.git
cd eos_snmpext
python setup.py bdist_rpm

scp dist/eos_snmpext-0.1.0-1.noarch.rpm <username>@<switch>:/tmp/

ssh <username>@<switch>

! clean up old extension
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

Usage
-----

For testing


Extending
---------
