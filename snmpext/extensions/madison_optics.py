# -*- coding: utf-8 -*-

import json
import re
from eos_snmpext.util import cli, platform

'''
+---interfaces
    |
    +--- Ethernet<number>
    |    |
    |    +--- residualISI
    |    |    |
    |    |    +---channels
    |    |    |   |
    |    |    |   +---1
    |    |    |   +---2
    |    |    +---unit
    |    |    |
    |    +--- uncorrectedBERCurr
    |    |    |
    |    |    +---channels
    |    |    |    |
    |    |    |    +---."-"
    |    |    +--unit
    |    |
    |    +--- laserFreq
    |    |    |
    |    |    +---channels
    |    |    |   |
    |    |    |   +---1
    |    |    |   +---2
    |    |    +---unit
    |    |    |
    |    +--- snr
    |    |    |
    |    |    +---channels
    |    |    |   |
    |    |    |   +---1
    |    |    |   +---2
    |    |    +---unit
    |    |    |
    |    +--- pam4Transitions
    |    |    |
    |    |    +---channels
    |    |    |   |
    |    |    |   +---1
    |    |    |   +---2
    |    |    +---unit
    |    |    |
    |    +--- preFecBERCurr
    |    |    |
    |    |    +---channels
    |    |    |    |
    |    |    |    +---."-"
    |    |    +--unit
    |    |
    |    +--- tecCurrent
    |    |    |
    |    |    +---channels
    |    |    |   |
    |    |    |   +---1
    |    |    |   +---2
    |    |    +---unit
'''


POLLING_INTERVAL = 5


def update(pp):

    response = cli("show interfaces transceiver dom | json")
    data = json.loads(response)

    sensors = ["residualISI", "uncorrectedBERCurr", "laserFreq", "snr", "pam4Transitions", "preFecBERCurr", "tecCurrent"]

    for interface, values in data["interfaces"].iteritems():
        
        #if_mib = re.search(r"\[([0-9_]+)\]", cli("show snmp mib walk 1.3.6.1.2.1.31.1.1.1.1 | grep {}".format(interface)))
        #interface_oid = if_mib.group(1)

        interface_oid = interface.replace("/", "")[8:]
        pp.add_str("{}".format(int(interface_oid)), interface)
        
        for sensor, readings in values["parameters"].iteritems():

            if sensor in sensors:
                idx = sensors.index(sensor)
                pp.add_str("{}.{}".format(int(interface_oid), idx), "{}".format(sensor))

                for channel,  number in readings.iteritems():
                    i = 1

                    if isinstance(number, dict):
                        pp.add_str("{}.{}.1".format(int(interface_oid), idx), "{}".format(channel))

                        for k, v in number.iteritems():
                            pp.add_str("{}.{}.1.{}".format(int(interface_oid), idx, i), "{}".format(str(v)))
                            i = i + 1

                    else:
                        pp.add_str("{}.{}.2".format(int(interface_oid), idx, i+1), "{}".format(str(number)))
