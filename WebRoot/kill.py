import HaloRadio.TopWeb as TopWeb

class plugin(TopWeb.TopWeb):
        def GetReqs(self):
		if self.config['general.guest_has_kill'] == "1":
			return "amvUG"
		else:
			return "amv"

	def handler(self, context):
		import HaloRadio.Util as Util
		import HaloRadio.Kill as Kill
		import HaloRadio.User as User
		import HaloRadio.Config as Config
		import HaloRadio.PlayHistListMaker as PlayHistListMaker

		songid=0

		if self.form.has_key("songid"):
                        songid = int(self.form['songid'].value)

		cfg=Config.Config()
		cur_song_id = int(songid)
		u = User.User(self.session.userid)
		if songid == 0:
			if self.do_authorize(u.rights,"a"):
				k = Kill.Kill(0, cur_song_id, self.session.userid )
		elif not self.do_authorize(u.rights,"GU") or self.config['general.guest_has_kill'] == "1":
			phlm = PlayHistListMaker.PlayHistListMaker()
			phlm.GetRecentPlays(1)
			ph = phlm.GetPlayHist(0)
			if ph.requestby == 0:
				k = Kill.Kill(0, cur_song_id, self.session.userid )
			elif ph.requestby == u.id or self.do_authorize(u.rights,"am"):
				k = Kill.Kill(0, cur_song_id, self.session.userid )



		request_url = "%s?action=CurrentInfo" % ( self.config['general.cgi_url'] )

		context.addGlobal ("refresh", "2;URL=%s" % ( request_url ) )
		context.addGlobal ("requesturl", request_url )


