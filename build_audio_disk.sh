#!/bin/sh
#
#

USER=$1
CDNUM=$2

TMPDIR=`mktemp -d -p ./`

nice ./file_list.py -u ${USER} -C ${CDNUM} > ${TMPDIR}/000_index.txt
cat ${TMPDIR}/000_index.txt | nice sh cpfiles.sh ${TMPDIR}

(
  cd ${TMPDIR}
  echo -ne "CD_DA\n\n" > 000_index.toc
  for file in *.mp3; do
    nice lame --decode ${file} ${file}.wav && \
     echo -ne "TRACK AUDIO\nSILENCE 00:01:00\nSTART\nFILE \"${file}.wav\" 0\n\n"\
        >> 000_index.toc
    rm -f ${file}
  done
  normalize -m *.wav
)

rm -rf ./top-audio-${USER}-${CDNUM}
mv ${TMPDIR} ./top-audio-${USER}-${CDNUM}


