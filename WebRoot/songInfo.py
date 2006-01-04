import HaloRadio.TopWeb as TopWeb
import HaloRadio.Song as Song
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
		if self.config['general.guest_has_songnfo'] == "1":
                	return "amvUG"
		else:
                	return "amv"
	def handler(self, context):
		if self.form.has_key("id"):
			songid = self.form['id'].value
		else:
			raise "songInfo without an id, duh!"
		s = Song.Song( songid )
		context.addGlobal ("sngname", s.GetDisplayName() )
		context.addGlobal ("path", s.path )
		context.addGlobal ("id3artist", s.artist )
		context.addGlobal ("id3album", s.album )
		context.addGlobal ("id3track", s.track )
		context.addGlobal ("id3title", s.GetDisplayName() )
		context.addGlobal ("id3genre", s.genre )
		context.addGlobal ("id3year", s.year )
		context.addGlobal ("id3comment", s.comment )
		context.addGlobal ("mpegver", s.mpeg_version )
		context.addGlobal ("mpegbr", s.mpeg_bitrate )
		context.addGlobal ("mpegsr", s.mpeg_samplerate )
		context.addGlobal ("mpeglen", s.GetDisplayLength() )
		context.addGlobal ("mpegmode", s.mpeg_mode )
		context.addGlobal ("mpegemph", s.mpeg_emphasis )
		context.addGlobal ("requests", s.requests )
		context.addGlobal ("plays", s.plays )
		context.addGlobal ("kills", s.kills )
		context.addGlobal ("requesturl", "%s?action=request&songids=%s"%(self.config['general.cgi_url'],s.id) )
		context.addGlobal ("downloadurl", "%s/%s" % (self.config['general.download_url'], s.path ) )

		import HaloRadio.UserSongStatsListMaker as UserSongStatsListMaker
		import HaloRadio.UserSongStats as UserSongStats
		import HaloRadio.User as User

		usslm = UserSongStatsListMaker.UserSongStatsListMaker()
		usslm.GetBySong(s.id)
		killedby = []
		requestedby = []
		for ussid in usslm.list:
			uss = UserSongStats.UserSongStats(ussid)
			try:
				user = User.User(uss.userid)
				username = user.GetDisplayName()
			except:
				username="**UNKNOWN**"

			if uss.kills > 0:
				kentity = {}
				kentity['name'] = username
				kentity['num'] = uss.kills
				killedby.append(kentity)
			if uss.requests > 0:
				rentity = {}
				rentity['name'] = username
				rentity['num'] = uss.requests
				requestedby.append(rentity)
		context.addGlobal ("killedby", killedby )
		context.addGlobal ("requestedby", requestedby )
