#!/usr/bin/python

#
# file_list.py - give a list of filenames in the givin playlist
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


#
#
# ./file_list.py 1 | perl -e 'while (<>){ chomp; print "\"$_\" \n";}' | xargs du -sch | grep total
#

import sys,getopt,os
import HaloRadio
import HaloRadio.Song as Song
def usage():
	print """
 file_list.py [-P|-U|-p <n>|-u <n>] [-t <n>|-C <n>]

	-P, --list-playlists
	-U, --list-users
        -p <number>, --playlist=
	-u <number>, --user=
	-t <number>, --top=
	-C <number>, --cdnum=
	-s <number>, --size=
"""
try: 
	opts,args = getopt.getopt( sys.argv[1:], "hPUp:t:u:C:s:", [ "help", "list-playlists", "list-users", "playlist=", "top=", "user=", "cdnum=", "size="])
except:

	usage()
	sys.exit(2)

playlist=0
user=0
top=0
list_playlists=0
list_users=0
cd_num=0
cd_size=0
for o, a in opts:
        if o in ("-h", "--help"):
	                usage()
			sys.exit(0)
        if o in ("-P", "--list-playlists"):
	                list_playlists = 1
        if o in ("-U", "--list-users"):
	                list_users = 1
	if o in ("-p", "--playlist"):
			playlist=int(a)
	if o in ("-t", "--top"):
			top=int(a)
	if o in ("-u", "--user"):
			user=a
	if o in ("-C", "--cdnum="):
			cd_num=int(a)
	if o in ("-s", "--size="):
			cd_size=int(a)
	
	
if list_playlists != 0:
	import HaloRadio.Playlist as Playlist
	import HaloRadio.PlaylistListMaker as PlaylistListMaker
	plm = PlaylistListMaker.PlaylistListMaker()
	plm.GetAll()
	print "system playlists :"
	for plid in plm.list:
		p = Playlist.Playlist(plid)
		print " %d: %s" % ( plid ,p.GetDisplayName() )
	sys.exit(1)
elif list_users != 0:
        import HaloRadio.User as User
        import HaloRadio.UserListMaker as UserListMaker
        ulm = UserListMaker.UserListMaker()
        ulm.GetAll()
        print "system users :"
        for ulid in ulm.list:
                u = User.User(ulid)
                print " %d: %s" % ( ulid ,u.GetDisplayName() )
        sys.exit(1)

elif playlist != 0:
	import HaloRadio.Playlist as Playlist
	import HaloRadio.Song as Song
	cur_playlist=Playlist.Playlist( playlist )
	cur_playlist.GetList()
	for i in cur_playlist.list:
		s = Song.Song( i)
		print "%s/%s" % ( HaloRadio.conf['path.root'],s.path )


elif user != 0:

	import HaloRadio.UserListMaker as UserListMaker
	import HaloRadio.UserSongStatsListMaker as UserSongStatsListMaker
	import HaloRadio.UserSongStats as UserSongStats
	import HaloRadio.User as User
	import HaloRadio.Song as Song

	ulm = UserListMaker.UserListMaker()
	usslm = UserSongStatsListMaker.UserSongStatsListMaker()

	ulm.GetByName(user)
	try:
		userid = ulm.GetUser(0).id
	except:
		print "ERROR: %s not found." % (user)
		sys.exit(100)

	if cd_num == 0:
		usslm.GetTopRank(userid, top)
		for (songid, requests, kills ) in usslm.list:
			try:
				s = Song.Song(songid)
			except:
				usslm2 = UserSongStatsListMaker.UserSongStatsListMaker()
				usslm2.GetBySong(songid)
				for id in usslm2.list:
					uss = UserSongStats.UserSongStats(id)
					uss.Delete()
			print "%s/%s" % ( HaloRadio.conf['path.root'],s.path )
	elif cd_size != 0:
		usslm.GetTopRank(userid, 102400)
		s = 0
		cd = 1
		cd_length = (1024*1024*cd_size)
		length = 0
		
		for (songid, requests, kills ) in usslm.list:
			try:
				s = Song.Song(songid)
			except:
				usslm2 = UserSongStatsListMaker.UserSongStatsListMaker()
				usslm2.GetBySong(songid)
				for id in usslm2.list:
					uss = UserSongStats.UserSongStats(id)
					uss.Delete()
				continue
			mysize =os.stat("%s/%s" % ( HaloRadio.conf['path.root'],s.path ))[6]
			if length + mysize > cd_length:
				cd = cd + 1
				length = 0
			length=length+mysize
			if cd == cd_num:
				print "%s/%s" % ( HaloRadio.conf['path.root'],s.path )
			elif cd > cd_num:
				sys.exit(0)

	else:
		usslm.GetTopRank(userid, 102400)
		length = 0
		cd = 1
		cd_length = (80 * 60)

		for (songid, requests, kills ) in usslm.list:
			s = Song.Song(songid)
			if length + s.mpeg_length > cd_length:
				cd = cd + 1
				length = 0
			length=length+s.mpeg_length
			if cd == cd_num:
				print "%s/%s" % ( HaloRadio.conf['path.root'],s.path )
			elif cd > cd_num:
				sys.exit(0)



elif top != 0:
	import HaloRadio.SongListMaker as SongListMaker

	slm = SongListMaker.SongListMaker()
	slm.GetTopRank(top)

	for i in slm.list:
		s = Song.Song( i)
		print "%s/%s" % ( HaloRadio.conf['path.root'],s.path )
else:
	usage()
