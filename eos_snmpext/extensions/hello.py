# -*- coding: utf-8 -*-

ROOT_OID = 255
POLLING_INTERVAL = 10

def update(pp):
    pp.add_str("%d.0" % ROOT_OID, 'Hello World!')
