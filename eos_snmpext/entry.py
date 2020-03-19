#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import argparse
import errno
import functools
import os
import pkgutil
import sys
import time

import eos_snmpext.extensions
import Logging
import Tac
from eos_snmpext.contrib import snmp_passpersist

# ====================
BASE_POLLING_INTERVAL = 1
MAX_RETRY = 10
NET_SNMP_EXTEND_OID = ".1.3.6.1.4.1.8072.1.3.1"
BASE_OID = NET_SNMP_EXTEND_OID + ".5"
# search these paths for the 'snmpext' directory
PATHS = ['/mnt/flash', '/persist/local']
# ====================

Tac.singleton("Tac::LogManager").syslogFacility = 'logLocal4'
Logging.logD(id="SYS_SNMPEXT_INFO",
             severity=Logging.logInfo,
             format="%s",
             explanation="[ Informational log message ]",
             recommendedAction=Logging.NO_ACTION_REQUIRED)

Logging.logD(id="SYS_SNMPEXT_EXTENSION_LOADED",
             severity=Logging.logInfo,
             format="%s",
             explanation="[ ]",
             recommendedAction=Logging.NO_ACTION_REQUIRED)

Logging.logD(id="SYS_SNMPEXT_EXTENSION_NOTSUPPORTED",
             severity=Logging.logNotice,
             format="%s",
             explanation="[ ]",
             recommendedAction=Logging.NO_ACTION_REQUIRED)

Logging.logD(id="SYS_SNMPEXT_UPDATING",
             severity=Logging.logDebug,
             format="%s",
             explanation="[ ]",
             recommendedAction=Logging.NO_ACTION_REQUIRED)

Logging.logD(id="SYS_SNMPEXT_SHUTDOWN",
             severity=Logging.logInfo,
             format="%s",
             explanation="[ ]",
             recommendedAction=Logging.NO_ACTION_REQUIRED)

Logging.logD(id="SYS_SNMPEXT_PIPE_CLOSED",
             severity=Logging.logError,
             format="%s",
             explanation="[ ]",
             recommendedAction=Logging.NO_ACTION_REQUIRED)

Logging.logD(id="SYS_SNMPEXT_RETRYING",
             severity=Logging.logWarning,
             format="%s",
             explanation="[ ]",
             recommendedAction=Logging.NO_ACTION_REQUIRED)

Logging.logD(id="SYS_SNMPEXT_RETRIES_EXHAUSTED",
             severity=Logging.logError,
             format="%s",
             explanation="[ ]",
             recommendedAction=Logging.NO_ACTION_REQUIRED)

PACKAGES = [eos_snmpext.extensions]
LAST_INTERVAL = {}

for path in PATHS:
    path = os.path.abspath(os.path.expanduser(path))

    if not os.path.exists(path):
        continue

    if path not in sys.path:
        sys.path.insert(1, path)

try:
    import snmpext
    PACKAGES.insert(0, snmpext)
except ImportError:
    pass

# See: https://mail.python.org/pipermail/tutor/2003-November/026645.html
class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)
sys.stderr = Unbuffered(sys.stderr)

def _load_extensions(names):
    modules = []
    for package in PACKAGES:
        for importer, name, ispkg in pkgutil.iter_modules(package.__path__, ''):

            if names and name not in names:
                # skip if name does not match 'names' passed by user
                continue

            full_name = ".".join([package.__name__, name])
            module = importer.find_module(name).load_module(full_name)

            if not hasattr(module, 'update'):
                continue

            if not is_supported(module):
                continue

            Logging.log(SYS_SNMPEXT_EXTENSION_LOADED, "Loaded extension: %s" % name)
            modules.append(module)
    return modules

def is_supported(extension):

    if not hasattr(extension, 'supported'):
        return True

    if not extension.supported():
        Logging.log(SYS_SNMPEXT_EXTENSION_NOTSUPPORTED,
                    "extension '%s' is not supported" % extension.__name__)
        return False
    
    return True

def update(pp, extensions):
    polling_interval = 0
    last_interval = 0

    for ext in extensions:
        now = time.time()

        if hasattr(ext, 'POLLING_INTERVAL'):
            polling_interval = ext.POLLING_INTERVAL

        if hasattr(ext, '_LAST_INTERVAL'):
            last_interval = ext._LAST_INTERVAL

        if now - last_interval >= polling_interval:
            Logging.log(SYS_SNMPEXT_UPDATING, "Polling timer expired, updating %s" % ext.__name__)
            ext.update(pp)
            ext._LAST_INTERVAL = now

def main():

    parser = argparse.ArgumentParser(prog="arcomm")
    arg = parser.add_argument

    arg("extensions", nargs="*", default=[])
    
    args = parser.parse_args()

    extensions = _load_extensions(args.extensions)
    retry_counter = MAX_RETRY

    while retry_counter > 0:
        message = ""
        try:
            pp = snmp_passpersist.PassPersist(BASE_OID)
            func = functools.partial(update, pp, extensions)
            pp.start(func, BASE_POLLING_INTERVAL)
        except KeyboardInterrupt:

            Logging.log(SYS_SNMPEXT_SHUTDOWN, "Exiting on user request")
            sys.exit(0)
        except IOError as exc:
            if exc.errno == errno.EPIPE:
                message = "snmpd has closed the pipe"
                Logging.log(SYS_SNMPEXT_PIPE_CLOSED, message)
                sys.exit(0)
        except EOFError as exc:
            Logging.log(SYS_SNMPEXT_SHUTDOWN, "EOF. shutting down...")
            sys.exit(0)

        Logging.log(SYS_SNMPEXT_RETRYING, message)

        retry_counter -= 1

    if retry_counter == 0:
        Logging.log(SYS_SNMPEXT_RETRIES_EXHAUSTED, "too many retrys, exiting")
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
