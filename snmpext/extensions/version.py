# -*- coding: utf-8 -*-

import os
from snmpext.util import is_mock_mode
from snmpext import __version__ as ver
ROOT_OID = 255
POLLING_INTERVAL = 86400 * 365

"""
"""

def update(pp):
    pp.add_str("%d.0" % ROOT_OID, "snmpext v%s" % ver)
