#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2016 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

from __future__ import absolute_import, division, print_function

import argparse
import errno
import functools
import os
import sys

from attr import has

try:
    import Logging
    import Tac
except ImportError:
    from snmpext.mock import Logging, Tac
    os.environ["SNMPEXT_MOCK_MODE"] = "1"

from snmpext import snmp_passpersist as snmp

# ====================
POLLING_INTERVAL = 30
MAX_RETRY = 10
NET_SNMP_EXTEND_OID = ".1.3.6.1.4.1.8072.1.3.1"
# search these paths for the 'snmpext' directory
# PATHS = ['/mnt/flash', '/persist/local']
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


def _load_extension(name):
    extension = None

    try:
        extension = getattr(__import__(
            "snmpext.extensions", fromlist=[name]), name)
    except AttributeError:
        raise ValueError("Failed to load extension '%s'" % name)

    Logging.log(SYS_SNMPEXT_EXTENSION_LOADED, "Loaded extension: %s" % name)

    return extension


def is_supported(extension):

    if not hasattr(extension, 'supported'):
        return True

    if not extension.supported():
        Logging.log(SYS_SNMPEXT_EXTENSION_NOTSUPPORTED,
                    "extension '%s' is not supported" % extension.__name__)
        return False

    return True


def run(extension):
    
    # extension.BASE_OID
    retry_counter = MAX_RETRY
    polling_interval = POLLING_INTERVAL
    base_oid = NET_SNMP_EXTEND_OID

    extension = _load_extension(extension)

    if hasattr(extension, "POLLING_INTERVAL") and extension.POLLING_INTERVAL > 0:
        polling_interval = extension.POLLING_INTERVAL

    while retry_counter > 0:
        message = ""
        try:
            pp = snmp.PassPersist(base_oid)
            pp.start(functools.partial(extension.update, pp), polling_interval)
        except KeyboardInterrupt:
            Logging.log(SYS_SNMPEXT_SHUTDOWN, "Exiting on user request")
            return 0
        except IOError as exc:
            if exc.errno == errno.EPIPE:
                message = "snmpd has closed the pipe"
                Logging.log(SYS_SNMPEXT_PIPE_CLOSED, message)
                return 0
        else:
            Logging.log(SYS_SNMPEXT_SHUTDOWN,
                        "Pass-persist has shut down, restarting")

        retry_counter -= 1

    if retry_counter == 0:
        Logging.log(SYS_SNMPEXT_RETRIES_EXHAUSTED, "too many retrys, exiting")
        return 1

    return 0


def main():
    import sys
    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    _, extension = script_name.split("-", 1)

    ret_code = run(extension)

    sys.exit(ret_code)

if __name__ == "__main__":
    main()
