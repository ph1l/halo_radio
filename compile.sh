#!/bin/sh
#
# this file is brought to yuo by the governator !!!
#
# kinda silly to have it be a shell script and all,
# but i just grabbed this from somewhere, so :-P.
#
# oh yea, this scans the current directory and children for
# .py's and compiles them to .pyc's
#

if [ -z $1 ]; then
	DIR="."
else
	DIR=$1
fi

compile='import py_compile, sys; py_compile.compile(sys.argv[1])'
find ${DIR} -type f -name '*.py' | xargs -n 1 python -c "$compile"
