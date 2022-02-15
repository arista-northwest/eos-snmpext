#!/bin/sh

DIR=/mnt/flash/snmpext

if [ -d $DIR ]; then
    rmddir -rf $DIR
fi
