#!/bin/sh

DIR=/var/tmp

if [ -d "$DIR" ]; then
    ln -sf /usr/bin/snmpext $DIR/snmpext
fi
