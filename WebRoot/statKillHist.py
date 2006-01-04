import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amv"
	def handler(self, context):
		import HaloRadio.KillHistListMaker as KillHistListMaker
		import HaloRadio.KillHist as KillHist
		import HaloRadio.Kill as Kill
		import HaloRadio.Exception as HaloException

		khlm = KillHistListMaker.KillHistListMaker()
		khlm.GetRecent(25)
		kills = []
		for killhistid in khlm.list:
			killhist = KillHist.KillHist(killhistid)
			try:
			    song = killhist.GetSong()
			except HaloException.SongNotFound:
			    continue
			    
			user = killhist.GetUser()
			entity = {}
			entity['songlink'] = "%s?action=songInfo&id=%s" % ( self.config['general.cgi_url'], song.id )
			entity['songname'] = song.GetDisplayName()
			entity['username'] = user.GetDisplayName()
			entity['userlink'] = "%s?action=userInfo&id=%s" % (self.config['general.cgi_url'], user.id )
			entity['date'] = killhist.date
			kills.append(entity)
		context.addGlobal ("killlist", kills)

