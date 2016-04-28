#!/bin/sh

DIR=/var/tmp
if [ -d "$DIR/snmpext" ]; then
    rm $DIR/snmpext
fi
