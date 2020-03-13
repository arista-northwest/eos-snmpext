#!/bin/sh

DIR=/var/tmp
if [ -L "$DIR/snmpext" ]; then
    rm $DIR/snmpext
fi
