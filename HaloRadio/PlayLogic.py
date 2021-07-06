#
#
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

import HaloRadio.Exception as Exception
import HaloRadio.Util as Util
import HaloRadio

class PlayLogic:
	"""
	- PlayLogic -
	This Class is a place to abstract Song Selection Logic. mostly used
	from radiod.py
	"""

	def __init__( self ):
		pass

	def GetKillState( self ):
		"""
		- PlayLogic.GetKillState() -
		  check pending kill requests. process the stats, if and of the
		requests is the current song, return true, else false.
		there could be more than one.
		"""

		import HaloRadio.KillListMaker as KillListMaker
		import HaloRadio.Config as Config
		import HaloRadio.Song as Song

		klm = KillListMaker.KillListMaker()
		cfg = Config.Config()
		
		bool = 0
		kills = klm.GetKills()
		try:
			cur_sid = int(cfg.GetConfigItem("current_song"))
		except:
			return bool

		import HaloRadio.User as User
		import HaloRadio.KillHist as KillHist
		import HaloRadio.PlayHistListMaker as PlayHistListMaker
		for kill in kills:
			kill.Delete()
			if kill.songid == 0:
				kuser = User.User(kill.requestby)
				if Util.do_authorize(kuser.rights, "a"):
					bool=1
					return 1

			try:
				phlm = PlayHistListMaker.PlayHistListMaker()
				phlm.GetRecentPlays(1)
				ph = phlm.GetPlayHist(0)
				song = Song.Song( kill.songid )
			except Exception.SongNotFound:
				pass
			if song.id == cur_sid:
				if ph.requestby == 0:
					bool=1
				elif ph.requestby == 1:
					bool = 1
				elif ph.requestby > 1:
					kuser = User.User(kill.requestby)
					ruser = User.User(ph.requestby)
					if Util.do_authorize(kuser.rights, "am"):
						bool=1
					elif kuser.id == ruser.id:
						bool=1
					else:
						bool=0
		if bool:
			song.UpdateKills()
			KillHist.KillHist(0,kill.songid,kill.requestby)
			u = User.User(kill.requestby)
			u.UpdateKills()
			import HaloRadio.UserSongStats as UserSongStats
			uss = UserSongStats.UserSongStats(0, u.id, song.id )
			uss.UpdateKills()

		return bool

	def GetNextSong( self ):
		"""
		- PlayLogic.GetNextSong() -
		  Shuffles through any requests or picks a random song
		from the current Playlist. returns a song object.
		"""

		import HaloRadio.RequestListMaker as RequestListMaker
		import HaloRadio.PlayHistListMaker as PlayHistListMaker
		import HaloRadio.PlaylistListMaker as PlaylistListMaker
		import HaloRadio.Playlist as Playlist
		import HaloRadio.Config as Config
		import time

		song = None
		request = None

		cfg = Config.Config()

		last_announce = int(cfg.GetConfigItem("last_announce"))
		announce_delay = int(HaloRadio.conf['general.announce_delay'])
		timestamp = time.time()
		if timestamp > last_announce + ( announce_delay * 60 ) :
			playlists = PlaylistListMaker.PlaylistListMaker()
			playlists.GetWhere( "name='Announce'")
			pl = Playlist.Playlist(playlists.Pop())

			try:
				song = pl.GetRandomSong()
			except Exception.SongNotFound, snf:
				print "caught a SongNotFound exception in PlayLogic... /me casts 'heal'"
				pl.DelSong(snf.id)
				
				song = self.GetNextSong()
			except Exception.PlaylistEmpty, ple:
				print "caught a PlaylistEmpty exception in PlayLogic... ignoring..."
			if song:
				song.Play(0)
				cfg.SetConfigItem("last_announce","%d"%(int(timestamp)))
				return song
			cfg.SetConfigItem("last_announce","%d"%(int(timestamp)))



		# First check if we have any requests,
		rlm = RequestListMaker.RequestListMaker()
		rlm.Get()
		if rlm.list != []:
			# if so take the next one
			request = rlm.GetNextRequest()
			if request != None:
				try:
					song = request.GetSong()
				except Exception.SongNotFound, snf:
					print "caught a SongNotFound exception in PlayLogic... /me casts 'heal'"
					request.Delete()
					
					song = self.GetNextSong()
				# Update the requests counter in the databse
				if request.requestby > 0:
					song.UpdateRequests()
					import HaloRadio.User as User
					u = User.User(request.requestby)
					u.UpdateRequests()
					import HaloRadio.UserSongStats as UserSongStats
					uss = UserSongStats.UserSongStats(0, u.id, song.id )
					uss.UpdateRequests()

				# delete it from the requests.
				request.Delete()

				song.Play(request.requestby)
		
		# else, one third of the time pick a song from active
		# users (if any)
		if request==None:
			import HaloRadio.SessionListMaker as SessionListMaker
			import HaloRadio.User as User
			import HaloRadio.Session as Session
			import random

			slm = SessionListMaker.SessionListMaker()
			slm.GetActive()
			song = None
			if len(slm.list) > 0 and int(HaloRadio.conf['general.active_user_weight']) > 0:
			    if random.randint(0,int(HaloRadio.conf['general.active_user_weight'])-1) == 0:
				userlist = []
				usernames = []
				for sessionid in slm.list:
					session = Session.Session(sessionid)
					user = User.User(session.userid)
					if user.id != 1 or user.requests < 100:
						userlist.append(user.id)
						usernames.append(user.GetDisplayName())
				if len(userlist) > 0:
					import HaloRadio.UserSongStatsListMaker as UserSongStatsListMaker
					usslm = UserSongStatsListMaker.UserSongStatsListMaker()
					try:
						song = usslm.GetRandomSongForUsers(userlist)
					except:
						print "Error getting user based song. no requests logged?"
					else:
						print "playing '%s' from users %s." %(
							song.GetDisplayName(),
							" ".join(usernames))
			if song == None:
				# pick a random song from the current playlist.
				curlistid = int( cfg.GetConfigItem("current_list") )
				pl = Playlist.Playlist(curlistid)
				try:
					song = pl.GetRandomSong()
				except Exception.SongNotFound, snf:
					print "caught a SongNotFound exception in PlayLogic... /me casts 'heal'"
					pl.DelSong(snf.id)
					song = self.GetNextSong()
			#
			# Checking Play History
			#

			played = 0
			phlm = PlayHistListMaker.PlayHistListMaker()
			phlm.GetRecentForTime(int(HaloRadio.conf['general.replay_limit']))
			for i in range(0,len(phlm.list)):
				ph = phlm.GetPlayHist(i)
				if ph.songid == song.id:
					print "song (%s) already played in the last %s minutes. skipping..." % (song.GetDisplayName(), HaloRadio.conf['general.replay_limit'])
					song = self.GetNextSong()
					played = 1
			if not played:
				song.Play(0)


		# return song object
		return song

