#!/usr/bin/env python

from __future__ import print_function
import os
import sh
import sys
import eapi

_, local, host = sys.argv[:3]

sess = eapi.session(host)

sh.scp(local, "admin@{}:/tmp/".format(host))

package = os.path.basename(local)

script = """no extension {0}
delete extension:{0}
""".format(package)
print(sess.send(script.splitlines()))

script = """copy file:/tmp/{0} extension:
extension {0}
copy installed-extensions boot-extensions
configure
no snmp-server extension .1.3.6.1.4.1.8072.1.3.1.5
snmp-server extension .1.3.6.1.4.1.8072.1.3.1.5 file:/var/tmp/snmpext
end
write
""".format(package)
print(sess.send(script.splitlines()))
