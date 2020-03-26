#!/bin/sh

DIR=/var/tmp

if [ -d "$DIR" ]; then
    ln -sf /usr/bin/snmpext $DIR/snmpext
    ln -sf /usr/bin/snmpext_mock $DIR/snmpext_mock
fi
