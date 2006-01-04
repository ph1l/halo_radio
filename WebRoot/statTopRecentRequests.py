import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amv"
	def handler(self, context):
		import HaloRadio.SongListMaker as SongListMaker
		import HaloRadio.Song as Song

                if self.form.has_key("num"):
                        num = int(self.form['num'].value)
                else:
                        num = 25
                if self.form.has_key("days"):
                        days = int(self.form['days'].value)
                else:
                        days = 7
		context.addGlobal ("num", num)
		context.addGlobal ("days", days)

		slm = SongListMaker.SongListMaker()
		slm.GetTopRequestsForTime(num,days)
		songs = []
		for songid in slm.list:
			try:
				song = Song.Song(songid)
				entity = {}
				entity['songlink'] = "%s?action=songInfo&id=%s" % ( self.config['general.cgi_url'], song.id )
				entity['songname'] = song.GetDisplayName()
				entity['recent_plays'] = song.GetNumRecentRequests(days)
				songs.append(entity)
			except:
				pass
		context.addGlobal ("songlist", songs)

