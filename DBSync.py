#!/usr/bin/python
#
# DBSync.py - fs sync util
#
#    Copyright (C) 2004-2010 Philip J Freeman
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

from string import find

import os,sys,time,getopt, re

import HaloRadio
import HaloRadio.Song as Song
import HaloRadio.SongListMaker as SongListMaker
import HaloRadio.PlaylistListMaker as PlaylistListMaker
import HaloRadio.Playlist as Playlist
import HaloRadio.Config as Config
#import HaloRadio.MP3Info as MP3Info
#import mmpython


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
	if dbversion<3:
		c = HaloRadio.db.cursor()
		c._do_query( """
ALTER TABLE `users` ADD COLUMN `enable` tinyint(1) DEFAULT 1;
			""")
		cfg.SetConfigItem("dbversion","3")
	if dbversion<4:
		cfg.NewConfigItem("moderator_enable_access","1");
		cfg.NewConfigItem("moderator_wall_enable_access","1");
		cfg.SetConfigItem("dbversion","4")
	if dbversion<5:
		c = HaloRadio.db.cursor()
		c._do_query( """
ALTER TABLE users ADD COLUMN active_time datetime;
			""")
		import HaloRadio.UserListMaker as ULM
		import HaloRadio.User as U
		ulm=ULM.UserListMaker()
		ulm.GetAll()
		for userid in ulm.list:
			u = U.User(userid)
			date = u.OldLastSeen()
			u.UpdateActivity(date)
		cfg.SetConfigItem("dbversion","5")
	if dbversion<6:
		c = HaloRadio.db.cursor()
		c._do_query( """
alter table songs change column mpeg_samplerate samplerate float unsigned default 0;
			""")
		c._do_query( """
alter table songs change column mpeg_length length mediumint(9) default 0;
			""")
		for column_name in ("mpeg_emphasis","mpeg_mode","mpeg_bitrate","mpeg_version"):
			c._do_query( """
alter table songs drop column %s;
			"""%(column_name))
		c._do_query( """
alter table songs add column mime tinytext;
			""")
		cfg.SetConfigItem("dbversion","6")
	return None

def check_dbversion():
	cfg = Config.Config()
	current_version=6

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

	from mutagen import File

	cfg = Config.Config()


	timenow = time.time()
	#print "timenow %s" % timenow

	if slow:
		#filestr = "find %s -follow -type f -name \"*.mp3\" " % ( arc_root )
		filestr = "find %s -follow -type f " % ( arc_root )
	else:
		try:
			lastupdatesecs=float(cfg.GetConfigItem("lastupdate"))
		except:
			lastupdatesecs=0

		#print "lastupdatesecs %s" % lastupdatesecs
		timediff = timenow - lastupdatesecs
		#print "timediff %s" % timediff

		#filestr = "find %s -type f -cmin -%d -name \"*.mp3\"" % ( arc_root, (timediff/60)+1 )
		filestr = "find %s -type f -cmin -%d " % ( arc_root, (timediff/60)+1 )
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
		try:
			songlist.SearchPath( path )
		except:
			log_message( verbose, "error searching db for: %s" % ( path ) )
			continue
		if ( len(songlist.list) > 1 ):
			for sid in songlist.list:
				song = Song.Song( sid )
				print "#%d:%s" % ( sid, song.path )
			raise "you got a problem here."
		#print file
		try: nfo = File(file)
		except AttributeError: print "%s:- Unknown file type"%(file)
		except KeyboardInterrupt: raise
		except Exception, err: print "%s:%s"%(file,str(err))
		try:
			samplerate = float(nfo.info.sample_rate)
		except:
			print "#Invalid MPEG samplerate:", file
			continue
		try:
			length = float(nfo.info.length)
		except:
			print "#Invalid MPEG length:", file
			continue
		try:
			mime = nfo.mime[0]
		except:
			print "#Invalid mime/type:", file
			continue
		if nfo.tags != None:
		    if nfo.tags.has_key('TPE1'):
			artist = nfo.tags['TPE1'].text[0].encode('ascii', 'replace')
		    elif nfo.tags.has_key('artist'):
			artist = nfo.tags['artist'][0].encode('ascii', 'replace')
		    else:
			artist = ""
		    if nfo.tags.has_key('TALB'):
			album = nfo.tags['TALB'].text[0].encode('ascii', 'replace')
		    elif nfo.tags.has_key('album'):
			album = nfo.tags['album'][0].encode('ascii', 'replace')
		    else:
			album = ""
		    if nfo.tags.has_key('TIT1'):
			title = nfo.tags['TIT1'].text[0].encode('ascii', 'replace')
		    elif nfo.tags.has_key('TIT2'):
			title = nfo.tags['TIT2'].text[0].encode('ascii', 'replace')
		    elif nfo.tags.has_key('title'):
			title = nfo.tags['title'][0].encode('ascii', 'replace')
		    else:
			title = ""
		    if nfo.tags.has_key('TRCK'):
			track = nfo.tags['TRCK'].text[0].encode('ascii', 'replace')
		    elif nfo.tags.has_key('tracknumber'):
			track = nfo.tags['tracknumber'][0].encode('ascii', 'replace')
		    else:
			track = "0"

		    if not track.find("/") == -1:
			pos = track.find("/")
			track = int(track[0:pos])
		    else:
			track = int(track)

		    if nfo.tags.has_key('TCON'):
			genre = nfo.tags['TCON'].text[0].encode('ascii', 'replace')
		    elif nfo.tags.has_key('genre'):
			genre = nfo.tags['genre'][0].encode('ascii', 'replace')
		    else:
			genre = ""

		    if nfo.tags.has_key('TDRC'):
			year = nfo.tags['TDRC'].text[0].encode('ascii', 'replace')
		    elif nfo.tags.has_key('date'):
			year = nfo.tags['date'][0].encode('ascii', 'replace')
		    else:
			year = ""
		    comment = ""
		else:
		    artist=""
		    album=""
		    title=""
		    track=0
		    genre=""
		    year = ""
		    comment = ""
			
		#print "%s %s %s %s %s %s"%(artist,album, title, track, genre, year)
		if ( len(songlist.list) > 0 ):
			song = Song.Song( songlist.list[0] )
			if (song.artist == artist) and (song.album== album) and (song.title== title) and (int(song.track) == int(track)) and (song.genre == genre) and (song.comment == comment) and (song.year == year) and ( song.mime==mime ) and ( int(song.samplerate) == int(samplerate) ) and (int(song.length) == int(length) ):
				continue
			else:
				log_message( verbose, 
					"fl:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s" % (
					artist,album,title,track,genre,comment,year,mime,samplerate,length)
				)
				log_message( verbose,
					"db:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s" % (
						song.artist,song.album,song.title,song.track,song.genre,song.comment,song.year,song.mime,song.samplerate,song.length)
					)
				print "#Updating", path
				song.Update(artist, album, title, track, genre, comment, year, mime, samplerate, length )
				continue
		
		print "#Adding", path
		song = Song.Song( 0, path, artist, album, title, track, genre, comment, year, mime, samplerate, length )
		log_message( verbose,
			"ad:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s" % (
				song.artist,song.album,song.title,song.track,song.genre,song.comment,song.year,song.mime,song.samplerate,song.length )
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
	playlists = PlaylistListMaker.PlaylistListMaker( )
	playlists.GetWhere( "name='Master'")
	try:
		playlist = Playlist.Playlist( playlists.Pop() )
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
	playlists = PlaylistListMaker.PlaylistListMaker( )
	playlists.GetWhere( "name='Requested'")
	try:
		playlist = Playlist.Playlist( playlists.Pop() )
	except:
		playlist = Playlist.Playlist( 0, "Requested" )

	playlist.Clear()
	reqested_songs = SongListMaker.SongListMaker( )
	reqested_songs.GetWhere("requests > 0")
	for songid in reqested_songs.list:
		playlist.AddSong( songid )


def make_smart_auto_playlist():
	playlists = PlaylistListMaker.PlaylistListMaker( )
	playlists.GetWhere( "name='AutoAI'")
	try:
		playlist = Playlist.Playlist( playlists.Pop() )
	except:
		playlist = Playlist.Playlist( 0, "AutoAI" )

	playlist.Clear()
	reqested_songs = SongListMaker.SongListMaker( )
	reqested_songs.GetWhere("requests > kills")
	for songid in reqested_songs.list:
		playlist.AddSong( songid )

def make_announce_playlist():
	playlists = PlaylistListMaker.PlaylistListMaker( )
	playlists.GetWhere( "name='Announce'")
	try:
		playlist = Playlist.Playlist( playlists.Pop() )
	except:
		playlist = Playlist.Playlist( 0, "Announce" )
	playlist.Clear()
	slm = SongListMaker.SongListMaker( )
	slm.GetWhere("""path LIKE "%s%%" """%(HaloRadio.conf['general.announce_path']))
	for songid in slm.list:
		playlist.AddSong( songid )

def do_scan_scale():
	r = re.compile('(\d+\.\d+)')
	all_songs = SongListMaker.SongListMaker( )
	all_songs.GetAll()
	for songid in all_songs.list:
		song=Song.Song(songid)
		if song.scale == 0:
			print "* %s : "%(song.path),
			cmd = "nice sox \"%s/%s\" -t null /dev/null stat -v 2>&1"%(arc_root,song.path)
			stat_stdout = os.popen( cmd,'r',)
			stat_out = stat_stdout.readline()
			while stat_out != '':
				m = r.match(stat_out)
				if m:
					song.UpdateScale(m.group(1))
					print m.group(1)
				stat_out = stat_stdout.readline()
			stat_stdout.close()

				
				
				


	
def usage():
	print
	print "%s: halo radio database sync'r" % ( os.path.basename(sys.argv[0] ) )
	print "	-h, --help	this cruft"
	print " -v, --verbose   print what we're doing"
	print "	-c, --clean	clean db"
	print "	-f, --scanfs	scan archive"
	print "	-s, --slow	slow search of fs"
	print " -p, --playlists	build playlists"
	print " -n, --normalize	scan mp3's to normalize"
	print


clean=0
slow=0
verbose=0
scanfs=0
playlists=0
normalize=0

check_dbversion()

try:
	opts, args = getopt.getopt( sys.argv[1:], "hcvsfpn", [ "help", "clean", "verbose", "slow", "scanfs", "playlists", "normalize" ])
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
	if o in ("-n", "--normalize"):
		normalize = 1
	#if o in ("-", "--"):
	#	 = 1


if not clean and not scanfs and not playlists and not normalize:
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

if normalize:
	log_message( 1, "normalizing...")
	do_scan_scale()
