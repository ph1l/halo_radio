#!/usr/bin/python
#
# DBSync.py - fs sync util
#    Copyright (C) 2004 Philip J Freeman
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

from string import find

import os,sys,time,getopt

import HaloRadio
import HaloRadio.Song as Song
import HaloRadio.SongListMaker as SongListMaker
import HaloRadio.Playlist as Playlist
import HaloRadio.Config as Config
import HaloRadio.MP3Info as MP3Info


arc_root=HaloRadio.conf['path.root']
arc_len=len(arc_root)+1

def check_string( string ):
      if string == None:
              return 1
      if len(string) > 255:
              return 1
      return 0

def make_printable_string( String ):
	newString = ""
	import string
	for i in range(0,len(String)):
		if String[i] in string.printable:
			newString += String[i]
	return newString
	
def update_dbversion():
	cfg = Config.Config()
	current_version=1

	dbversion=int(cfg.GetConfigItem("dbversion"))

	if dbversion<1:
		c = HaloRadio.db.cursor()
		c._do_query( """
ALTER TABLE `users` ADD COLUMN `style` int(10) DEFAULT 1;
			""")
		c._do_query( """
CREATE TABLE `styles` (
  `id` int(10) unsigned NOT NULL auto_increment,
  `style` tinytext NOT NULL,
  PRIMARY KEY (`id`)
) TYPE=MyISAM;
			""")
		c._do_query( """

INSERT INTO `styles` VALUES (1,'style.css');
			""")
		c._do_query( """
INSERT INTO `styles` VALUES (2,'no_style.css');
			""")
		c._do_query( """
INSERT INTO `styles` VALUES (3,'style_green.css');
			""")
		c._do_query( """
INSERT INTO `styles` VALUES (4,'style_pink.css');
			""")

		cfg.SetConfigItem("dbversion","1")
	if dbversion<2:
		c = HaloRadio.db.cursor()
		c._do_query( """
ALTER TABLE `users` ADD COLUMN `post` tinyint(1) DEFAULT 1;
			""")
		cfg.SetConfigItem("dbversion","2")
	return None

def check_dbversion():
	cfg = Config.Config()
	current_version=2

	try:
		dbversion=cfg.GetConfigItem("dbversion")
	except:
		print "WARNING: dbversion tag not found."
		print "       : Check that your DB structure is up to date."
		return 0

	dbversion=int(dbversion)

	if dbversion < current_version:
		print "WARNING: dbversion tag indicates your database is out of date. Updating..."
		update_dbversion()

	return 1

def update_db(slow, verbose=0):  

	cfg = Config.Config()


	timenow = time.time()
	#print "timenow %s" % timenow

	if slow:
		filestr = "find %s -follow -type f -name \"*.mp3\"" % ( arc_root )
	else:
		try:
			lastupdatesecs=float(cfg.GetConfigItem("lastupdate"))
		except:
			lastupdatesecs=0

		#print "lastupdatesecs %s" % lastupdatesecs
		timediff = timenow - lastupdatesecs
		#print "timediff %s" % timediff

		filestr = "find %s -type f -cmin -%d -name \"*.mp3\"" % ( arc_root, (timediff/60)+1 )
	cfg.SetConfigItem("lastupdate",str(timenow))
	#print filestr
	files=os.popen(filestr)
	
	line_in = files.readline()
	
	while ( line_in != "" ):
		file = line_in[:-1]		# chomp the \n
		line_in = files.readline()	# grab the next line
		path = file[arc_len:]		# cut the root off the filename

		# Check to see if this file is in the 
		#log_message( verbose, "file_in: %s" % ( path ) )
		songlist = SongListMaker.SongListMaker()
		songlist.SearchPath( path )
		if ( len(songlist.list) > 1 ):
			for sid in songlist.list:
				song = Song.Song( sid )
				print "#%d:%s" % ( sid, song.path )
			raise "you got a problem here."
		try:
			nfo = MP3Info.MP3Info(open(file, 'rb'))
		except:
			print "#Error Parsing file: "
			print """ls -la "%s" """%( file )
			continue

		if nfo.mpeg.valid != 1:
			print "#Invalid MPEG in File: %s" % ( file )
			print """ls -la "%s" """%( file )
			continue
		artist = ""
		year = ""
		comment = ""
		genre = ""
		track = 0
		title = ""
		album = ""
		if nfo.artist != None:
			artist = make_printable_string(nfo.artist)
		if nfo.album != None:
			album = make_printable_string(nfo.album)
		if nfo.title != None:
			title = make_printable_string(nfo.title)
		if nfo.track != None:
			track = nfo.track
		if nfo.genre != None:
			genre = nfo.genre
		if nfo.comment != None:
			comment = make_printable_string(nfo.comment)
		if nfo.year != None:
			year = nfo.year
		mpeg_version = nfo.mpeg.version
		mpeg_bitrate = nfo.mpeg.bitrate
		mpeg_samplerate = nfo.mpeg.samplerate
		mpeg_length = int ((nfo.mpeg.length_minutes*60 ) + nfo.mpeg.length_seconds)
		mpeg_emphasis = nfo.mpeg.emphasis
		mpeg_mode = nfo.mpeg.mode
		#if mpeg_samplerate != 44100:
		#	print "#Invalid mpeg_samplerate %s in File: %s" % ( mpeg_samplerate, file )
		#	print """ls -la "%s" """%( file )
		#	continue
		if comment:
			if find(comment,"iTunes") != -1:
				comment = "iTunes comment not added to database"
			if len(comment) > 1024:
				comment = "over 1024 bytes truncating."
		try:
			track = int(track)
		except:
			track = 0

		if ( len(songlist.list) > 0 ):
			song = Song.Song( songlist.list[0] )
			if (song.artist == artist) and (song.album== album) and (song.title== title) and (int(song.track) == int(track)) and (song.genre == genre) and (song.comment == comment) and (song.year == year) and ( song.mpeg_version == mpeg_version ) and ( int(song.mpeg_bitrate) == int(mpeg_bitrate) ) and ( int(song.mpeg_samplerate) == int(song.mpeg_samplerate) )and (int(song.mpeg_length) == int(mpeg_length) ) and (song.mpeg_emphasis == mpeg_emphasis) and (song.mpeg_mode == mpeg_mode):
				continue
			else:
				log_message( verbose, 
					"fl:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s" % (
					artist,album,title,track,genre,comment,year,mpeg_version,mpeg_bitrate,mpeg_samplerate,mpeg_length,mpeg_emphasis,mpeg_mode )
				)
				log_message( verbose,
					"db:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s" % (
						song.artist,song.album,song.title,song.track,song.genre,song.comment,song.year,song.mpeg_version,song.mpeg_bitrate,song.mpeg_samplerate,song.mpeg_length,song.mpeg_emphasis,song.mpeg_mode )
					)
				print "#Updating", path
				song.Update(artist, album, title, track, genre, comment, year, mpeg_version, mpeg_bitrate, mpeg_samplerate, mpeg_length, mpeg_emphasis, mpeg_mode )
				continue
		
		print "#Adding", path
		song = Song.Song( 0, path, artist, album, title, track, genre, comment, year, mpeg_version, mpeg_bitrate, mpeg_samplerate, mpeg_length, mpeg_emphasis, mpeg_mode )
		log_message( verbose,
			"ad:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s" % (
				song.artist,song.album,song.title,song.track,song.genre,song.comment,song.year,song.mpeg_version,song.mpeg_bitrate,song.mpeg_samplerate,song.mpeg_length,song.mpeg_emphasis,song.mpeg_mode )
			)

def clean_db(verbose=0):

		slm = SongListMaker.SongListMaker()
		slm.GetAll()
		for songid in slm.list:
			song = Song.Song(songid)
			if ( os.access(arc_root + "/" + song.path, os.R_OK)==0 ):
				song.Delete()
				print "#Deleted", song.path, "from the database"

def log_message(ifval,msg):
	if ifval:
		print "#",msg

def make_master_playlist():
	try:
		playlist = Playlist.Playlist( 1 )
	except:
		playlist = Playlist.Playlist( 0, "Master" )

	# delete any songs from playlist 1
	playlist.Clear()
	# add all songs to playlist 1
	all_songs = SongListMaker.SongListMaker( )
	all_songs.GetAll()
	for songid in all_songs.list:
		playlist.AddSong( songid )

def make_request_playlist():
	try:
		playlist = Playlist.Playlist( 2 )
	except:
		playlist = Playlist.Playlist( 0, "Requested" )

	playlist.Clear()
	reqested_songs = SongListMaker.SongListMaker( )
	reqested_songs.GetWhere("requests > 0")
	for songid in reqested_songs.list:
		playlist.AddSong( songid )


def make_smart_auto_playlist():
	try:
		playlist = Playlist.Playlist( 3 )
	except:
		playlist = Playlist.Playlist( 0, "AutoAI" )

	playlist.Clear()
	reqested_songs = SongListMaker.SongListMaker( )
	reqested_songs.GetWhere("requests > kills")
	for songid in reqested_songs.list:
		playlist.AddSong( songid )

def make_announce_playlist():
	try:
		playlist = Playlist.Playlist( 4 )
	except:
		playlist = Playlist.Playlist( 0, "Announce" )
	playlist.Clear()
	slm = SongListMaker.SongListMaker( )
	slm.GetWhere("""path LIKE "%s%%" """%(HaloRadio.conf['general.announce_path']))
	for songid in slm.list:
		playlist.AddSong( songid )

def usage():
	print
	print "%s: halo radio database sync'r" % ( os.path.basename(sys.argv[0] ) )
	print "	-h, --help	this cruft"
	print " -v, --verbose   print what we're doing"
	print "	-c, --clean	clean db"
	print "	-f, --scanfs	scan archive"
	print "	-s, --slow	slow search of fs"
	print " -p, --playlists	build playlists"
	print


clean=0
slow=0
verbose=0
scanfs=0
playlists=0

check_dbversion()

try:
	opts, args = getopt.getopt( sys.argv[1:], "hcvsfp", [ "help", "clean", "verbose", "slow", "scanfs", "playlists" ])
except getopt.GetoptError:
	usage()
	sys.exit(2)

for o, a in opts:
	if o in ("-h", "--help"):
		usage()
		sys.exit()
	if o in ("-v", "--verbose"):
		verbose = 1
	if o in ("-c", "--clean"):
		clean = 1
	if o in ("-s", "--slow"):
		slow = 1
	if o in ("-f", "--scanfs"):
		scanfs = 1
	if o in ("-p", "--playlists"):
		playlists = 1
	#if o in ("-", "--"):
	#	 = 1


if not clean and not scanfs and not playlists:
	usage()

if clean:
	log_message( 1, "checking files in db against disk...")
	clean_db(verbose)

if scanfs:
	log_message( 1, "checking files on disk against db...")
	update_db(slow, verbose)

if playlists:
	log_message( 1, "building playlists...")
	make_master_playlist()
	make_request_playlist()
	make_smart_auto_playlist()
	make_announce_playlist()

