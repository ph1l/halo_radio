#!/usr/bin/python
#
# simple hack to rename files in the db.
#
#  pass it a list of song ids (seerated by commas), a search sctring and a replacement
#
#

import string,os,sys,time,getopt

def usage():
	print " %s [--ids=<songid1>,<songid2>[,...]] --search=<old_str> --replace=<new_str>" % (sys.argv[0])
	sys.exit(2)

try:
        opts, args = getopt.getopt( sys.argv[1:], "hi:s:r:", [ "help", "ids=", "search=", "replace=" ])
except getopt.GetoptError:
        usage()
        sys.exit(2)
ids = None
search = None
replace = None

for o, a in opts:
        if o in ("-h", "--help"):
                usage()
                sys.exit()
	if o in ("-i", "--ids"):
		ids = a.split(",")
	if o in ( "-s", "--search"):
		search =  a
	if o in ( "-r", "--replace"):
		replace =  a

print "%s %s %s" % (ids,search,replace)

if ( search == None ) or  ( replace == None ):
	usage()

import HaloRadio

if ids == None:
	import HaloRadio.SongListMaker as SongListMaker
	slm = SongListMaker.SongListMaker()
	slm.GetAll()
	ids = slm.list
import HaloRadio.Song as Song
for sid in ids:
	s = Song.Song(sid)
	pos = s.path.find(search)
	if pos == -1:
		continue
	print "Matched %s." % (s.GetDisplayName())
	s.UpdatePath(s.path.replace(search,replace))
	print "Updated to %s." % (s.path)
print " done."






