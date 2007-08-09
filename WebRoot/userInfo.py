import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amv"
	def handler(self, context):
		import HaloRadio.UserSongStatsListMaker as UserSongStatsListMaker
		import HaloRadio.UserSongStats as UserSongStats
		import HaloRadio.Song as Song
		import HaloRadio.User as User
		import HaloRadio.Exception as Exception

		# Username
		if self.form.has_key("id"):
                        userid = int(self.form['id'].value)
			#if ( userid != self.user.id and
			#	not self.do_authorize(self.user.rights,"am")
			#):
			#	self.do_error("Unautherized")
		else:
			userid = self.user.id

		if self.form.has_key("numtop"):
			numtop = int(self.form['numtop'].value)
		else:
			numtop = 25
		if self.form.has_key("numbottom"):
			numbottom = int(self.form['numbottom'].value)
		else:
			numbottom = 25
		user = User.User(userid)
		context.addGlobal ("numtop", numtop )
		context.addGlobal ("numbottom", numbottom )
		context.addGlobal ("id",userid )
		context.addGlobal ("action", "userInfo"  )
		context.addGlobal ("username", user.GetDisplayName() )
		context.addGlobal ("rights", user.GetDisplayRights() )
		
		context.addGlobal ("createdate", user.create_time )
		seen = user.LastSeen()
		if not seen:
			seen = user.create_time;
		context.addGlobal ("seendate", seen)

		# Return my top 100
		slm = UserSongStatsListMaker.UserSongStatsListMaker()
		slm.GetTopRank(user.id,numtop)
		songs = []
		for (songid, requests, kills) in slm.list:
			try:
				song = Song.Song(songid)
			except Exception.SongNotFound:
				continue
			entity = {}
			entity['songlink'] = "%s?action=songInfo&id=%s" % ( self.config['general.cgi_url'], song.id )
			entity['songname'] = song.GetDisplayName()
			entity['requests'] = requests
			entity['kills'] = kills
			songs.append(entity)
		context.addGlobal ("songlist", songs)

		slm.GetBottomRank(user.id,numbottom)
		songs2= []
		for (songid, kills, requests) in slm.list:
			try:
				song = Song.Song(songid)
			except Exception.SongNotFound:
				continue
			entity = {}
			entity['songlink'] = "%s?action=songInfo&id=%s" % ( self.config['general.cgi_url'], song.id )
			entity['songname'] = song.GetDisplayName()
			entity['requests'] = requests
			entity['kills'] = kills
			songs2.append(entity)
		context.addGlobal ("bsonglist", songs2)
			

