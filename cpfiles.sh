#!/bin/sh
#
#

NUM=0

while read LINE; do
	NUM=$(($NUM + 1))
	cp -v "${LINE}" $1/`printf %03d ${NUM}`.mp3
done
