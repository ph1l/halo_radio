#!/bin/sh
#
#

USER=$1
CDNUM=$2

TMPDIR=`mktemp -d -p ./`

nice ./file_list.py -u ${USER} -s 699 -C ${CDNUM} > ${TMPDIR}/000_index.txt
cat ${TMPDIR}/000_index.txt | nice sh cpfiles.sh ${TMPDIR}

rm -rf ./top-mp3-${USER}-${CDNUM}.iso
nice mkisofs -o ./top-mp3-${USER}-${CDNUM}.iso -J -R ${TMPDIR}

rm -rf ${TMPDIR}

