#!/bin/sh

if [ -z $1 ]; then
	echo need a doc_root
	exit 2
else
	DEST=${1}
fi

echo -n "copying files to ${DEST}..."
cp -a favicon.ico styles/*.css sendmail.py .htaccess HaloRadio HaloRadio.cgi HaloRadio.ini WebRoot help CurrentInfo.js Timeout.html ${DEST}
echo -ne " done\n"
