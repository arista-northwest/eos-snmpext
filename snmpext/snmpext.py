# -*- coding: utf-8 -*-
# Copyright (c) 2023 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import errno
import functools
import os
import sys
from snmpext import _snmp_passpersist
from typing import Callable

try:
    import Logging
    import Tac
except ImportError:
    from snmpext.mock import Logging, Tac
    os.environ["SNMPEXT_MOCK_MODE"] = "1"

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

class PassPersist(_snmp_passpersist.PassPersist):

    # def __init__(self):
    #     base_oid = ""
    #     super().__init__(base_oid)

    def run(self, func: Callable[["PassPersist"], None], polling_interval: int = 1, max_retries: int = 3):
        Logging.log(SYS_SNMPEXT_INFO, "starting")
        while max_retries > 0:
            try:
                func = functools.partial(func, self)
                self.start(func, polling_interval)
            except KeyboardInterrupt:
                Logging.log(SYS_SNMPEXT_SHUTDOWN, "Exiting on user request")
                return
            except IOError as exc:
                if exc.errno == errno.EPIPE:
                    Logging.log(SYS_SNMPEXT_PIPE_CLOSED, "snmpd has closed the pipe")
                    return
            else:
                Logging.log(SYS_SNMPEXT_SHUTDOWN,
                            "Pass-persist has shut down, restarting")

            retry_counter -= 1

        if retry_counter == 0:
            Logging.log(SYS_SNMPEXT_RETRIES_EXHAUSTED, "too many retrys, exiting")
            return

        return

def run(base_oid: str, *args, **kwargs):
    se = PassPersist(base_oid)
    se.run(*args, **kwargs)