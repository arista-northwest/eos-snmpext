#!/usr/bin/env python

from __future__ import print_function
import os
import sh
import sys
import eapi

target = "snmpext.rpm"

_, local, host = sys.argv[:3]

sess = eapi.session(host)

sh.scp(local, "admin@{}:/tmp/{}".format(host, target))

#package = os.path.basename(local)

script = """configure
no snmp-server extension .1.3.6.1.4.1.8072.1.3.1.5
end
no extension {0}
delete extension:{0}
delete flash
""".format(target)
print(sess.send(script.splitlines()))

script = """copy file:/tmp/{0} extension:
extension {0}
copy installed-extensions boot-extensions
configure
snmp-server extension .1.3.6.1.4.1.8072.1.3.1.5 file:/var/tmp/snmpext
end
write
""".format(target)
print(sess.send(script.splitlines()))
