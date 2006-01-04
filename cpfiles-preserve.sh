#!/bin/sh
#
#

CUT_DIRS_NUM=4

DEST_DIR=./music

PLAYLIST=${DEST_DIR}/${1}.m3u

> ${PLAYLIST}

while read LINE; do

	TRIM=`echo "${LINE}" | cut -d/ -f${CUT_DIRS_NUM}-`
	echo ${TRIM} >> ${PLAYLIST}
	mkdir -p "${DEST_DIR}/${TRIM%/*.mp3}"
	cp "${LINE}" "${DEST_DIR}/${TRIM}"
done
