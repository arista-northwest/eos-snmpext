#!/bin/sh
DIR=/var/tmp

if [ -d "$DIR" ]; then
    cp /usr/bin/snmpext /var/tmp/snmpext
fi
