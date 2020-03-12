#!/bin/sh

DIR=/var/tmp

if [ -d "$DIR" ]; then
    if [ -f "$DIR/snmpext"]; then
        rm $DIR/snmpext
    fi
    ln -sf /usr/bin/snmpext $DIR/snmpext
fi
