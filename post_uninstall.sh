#!/bin/sh

DIR=/var/tmp
if [ -f "$DIR/snmpext" ]; then
    rm $DIR/snmpext
fi
