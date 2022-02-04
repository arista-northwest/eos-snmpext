# Copyright (c) 2020 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

import sys

logNull = None
logEmergency = 0
logAlert = 1
logCritical = 2
logError = 3
logWarning = 4
logNotice = 5
logInfo = 6
logDebug = 7

NO_ACTION_REQUIRED = "No action is required..."
CALL_SUPPORT_IF_PERSISTS = "If the problem persists, contact your suppor..."
CONTACT_SUPPORT = "This is a serious error..."

def logD( id, *args, **kwargs):
    # fakew how the real Logging modules ability to force the 'id' into scope
    sys._getframe(1).f_globals[id] = None

def log(handle, *args, **kwargs):
    pass