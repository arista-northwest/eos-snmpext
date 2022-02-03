#!/bin/sh

DIR=/mnt/flash/snmpext
#mkdir -p $DIR/{bin,extensions}
mkdir -p $DIR/bin
#touch $DIR/extentions/__init__.py
ln -sf /usr/bin/snmpext $DIR/bin/snmpext

