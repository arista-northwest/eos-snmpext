# -*- coding: utf-8 -*-

import os
from eos_snmpext.util import is_mock_mode

ROOT_OID = 255
POLLING_INTERVAL = 86400 * 365

def update(pp):
    s = "Hello World!"
    if is_mock_mode():
        s = "Mocked Hello World?"

    pp.add_str("%d.0" % ROOT_OID, s)
