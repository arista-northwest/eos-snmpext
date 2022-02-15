# -*- coding: utf-8 -*-

import os
from snmpext.util import is_mock_mode
from snmpext import __version__ as ver

BASE_OID = ".1.3.6.1.4.1.8072.1.3.1.5.255"
ROOT_OID = 255

"""
"""

def update(pp):
    pp.add_str("%d.0" % ROOT_OID, "snmpext v%s" % ver)
