# -*- coding: utf-8 -*-

from snmpext import PassPersist
from snmpext import __version__ as ver

BASE_OID = ".1.3.6.1.4.1.8072.1.3.1.5.255"

def update(pp: PassPersist):
    pp.add_str("%s.0" % BASE_OID, "Hello from: snmpext v%s" % ver)

if __name__ == "__main__":
    PassPersist(BASE_OID).run(update)