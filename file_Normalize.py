#!/usr/bin/python
#
# FIXME! DBSync.py - fs sync util
#    Copyright (C) 2004 Philip J Freeman
#
#    This file is part of halo_radio
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os,sys,time,getopt, re, string

import HaloRadio
import HaloRadio.Song as Song
import HaloRadio.SongListMaker as SongListMaker
import HaloRadio.Playlist as Playlist
import HaloRadio.Config as Config
#import HaloRadio.MP3Info as MP3Info
#import mmpython


arc_root=HaloRadio.conf['path.root']
arc_len=len(arc_root)+1
filename_valid_chars = string.letters + string.digits

def check_string( string ):
      if string == None:
              return 1
      if len(string) > 255:
              return 1
      return 0

def shell_escape_string( String ):
	newString = ""
	for i in range(0,len(String)):
		if String[i] in "\"":
			newString += "\\"+String[i]
		else:
			newString += String[i]
	return newString
	
def make_printable_string( String ):
	newString = ""
	for i in range(0,len(String)):
		if String[i] in string.printable:
			newString += String[i]
	return newString
	
def make_fn_string( String ):
	newString = ""
	for i in range(0,len(String)):
		if String[i] == " ":
			newString += "_"
		elif String[i] == "&":
			newString += "and"
		elif String[i] in filename_valid_chars:
			newString += String[i]
	return string.lower(newString)
	
def process_dir(dir,subroot, verbose=1, dry_run=1 ):  

	from mutagen import File


	filestr = "find %s/%s -follow -type f -name \"*.mp3\" " % ( arc_root, dir )
	#print filestr
	files=os.popen(filestr)
	
	line_in = files.readline()
	
	while ( line_in != "" ):
		file = line_in[:-1]		# chomp the \n
		line_in = files.readline()	# grab the next line
		path = file[arc_len:]		# cut the root off the filename

		# Check to see if this file is in the 
		log_message( verbose, "file_in: %s" % ( path ) )
		songlist = SongListMaker.SongListMaker()
		try:
			songlist.SearchPath( path )
		except:
			log_message( verbose, "ERR-NTFND: %s" % ( path ) )
			continue
		if ( len(songlist.list) > 1 ):
			for sid in songlist.list:
				song = Song.Song( sid )
				print "ERR-DUPE:%d:%s" % ( sid, song.path )
			continue
		#print file
		song = Song.Song( songlist.list[0] )
		## move files..
		fn_artist=make_fn_string(song.artist)
		fn_album =make_fn_string(song.album)
		fn_title =make_fn_string(song.title)
		log_message(verbose,"fn:%s:%s:%s"%(fn_artist,fn_album,fn_title))
		if fn_album == "":
			if fn_artist == "" or fn_title == "":
				print "#Skipping: ", song.path
				continue
			new_path="%s/%s/%s---%s.mp3"%(subroot,fn_artist,fn_artist,fn_title)
		elif song.track == 0:
			new_path="%s/%s/%s/%s-%s--%s.mp3"%(subroot,fn_artist,fn_album,fn_artist,fn_album,fn_title)
		else:
			new_path="%s/%s/%s/%s-%s-%02d-%s.mp3"%(subroot,fn_artist,fn_album,fn_artist,fn_album,song.track,fn_title)

		if new_path != song.path:
			log_message( verbose, 
				"nf:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s" % (
					song.artist,song.album,song.title,song.track,song.genre,song.comment,song.year,song.mime,song.samplerate,song.length )
				)
			new_dir = os.path.dirname(new_path)
			if dry_run == 0:
				if os.path.exists("%s/%s"%(arc_root,new_dir)) == False:
					if os.system("mkdir -pv %s/%s"%(arc_root,new_dir)) != 0:
						os.exit()
				log_message( verbose,"mv:%s:%s" % (song.path,new_path))
				if os.system("mv -v %s/\"%s\" %s/%s"%(arc_root,shell_escape_string(song.path),arc_root,new_path)) != 0:
					os.exit()
				song.UpdatePath(new_path)
			else:
				print "mv:%s:%s" % (song.path,new_path)
		else:
			print "mv:path unchanged"

def log_message(ifval,msg):
	if ifval:
		print "#",msg

def usage():
	print
	print "%s: halo radio database sync'r" % ( os.path.basename(sys.argv[0] ) )
	print "	-h, --help"
	print " -v, --verbose"
	print "	-s, --subroot    destination subdir"
	print " -n, --dry-run"
	print


verbose=0
dry_run=0
subroot="rooot"


try:
	opts, args = getopt.getopt( sys.argv[1:], "hvn", [ "help", "verbose", "dry-run" ])
except getopt.GetoptError:
	usage()
	sys.exit(2)

for o, a in opts:
	if o in ("-h", "--help"):
		usage()
		sys.exit()
	if o in ("-v", "--verbose"):
		verbose = 1
	if o in ("-n", "--dry-run"):
		dry_run = 1
	if o in ("-s", "--subroot"):
		subroot=a
	#if o in ("-", "--"):
	#	 = 1


for dir in args:
	process_dir(dir, subroot, verbose,dry_run)
