#!/usr/bin/env python

import os
import sh
import sys
import arcomm

_, local, host = sys.argv[:3]

sh.scp(local, "{}:/tmp/".format(host))

package = os.path.basename(local)

script = """
no extension {0}
delete extension:{0}
""".format(package)
print arcomm.execute('eapi://{}'.format(host), script.splitlines())

script = """
copy file:/tmp/{0} extension:
extension {0}
copy installed-extensions boot-extensions
configure
no snmp-server extension .1.3.6.1.4.1.8072.1.3.1.5
snmp-server extension .1.3.6.1.4.1.8072.1.3.1.5 file:/var/tmp/snmpext
end
write
""".format(package)

print arcomm.execute('eapi://{}'.format(host), script.splitlines())
