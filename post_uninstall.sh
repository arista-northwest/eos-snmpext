#!/bin/sh

DIR=/var/tmp
if [ -L "$DIR/snmpext" ]; then
    rm $DIR/snmpext

if [ -L "$DIR/snmpext_mock" ]; then
    rm $DIR/snmpext_mock
fi
