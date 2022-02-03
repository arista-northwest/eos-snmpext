#!/bin/sh

DIR=/mnt/flash/snmpext

if [ -d $DIR ]; then
    if [ -d $DIR/bin ]; then
        rm -f $DIR/bin/*
        rmdir $DIR/bin
    fi
    rmddir $DIR
fi
