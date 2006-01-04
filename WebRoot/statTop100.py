import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amvUG"
	def handler(self, context):
		import HaloRadio.SongListMaker as SongListMaker
		import HaloRadio.Song as Song

		slm = SongListMaker.SongListMaker()
		slm.GetTopRank(100)
		songs = []
		for songid in slm.list:
			song = Song.Song(songid)
			entity = {}
			entity['songlink'] = "%s?action=songInfo&id=%s" % ( self.config['general.cgi_url'], song.id )
			entity['songname'] = song.GetDisplayName()
			entity['requests'] = song.requests
			entity['kills'] = song.kills
			songs.append(entity)
		context.addGlobal ("songlist", songs)

