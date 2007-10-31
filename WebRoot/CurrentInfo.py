import HaloRadio.TopWeb as TopWeb
import HaloRadio.PlayHistListMaker as PlayHistListMaker
import HaloRadio.RequestListMaker as RequestListMaker
import HaloRadio.SessionListMaker as SessionListMaker
import HaloRadio.Exception as Exception
import HaloRadio.User as User
class plugin(TopWeb.TopWeb):
	def GetReqs(self):
		return "amvUG"

	def handler(self, context):

                if self.form.has_key("i"):
                        i = int(self.form['i'].value)
                else:
                        i = 0
		# this is for pat...
		if i < 0:
			i = 0
		i = i+1

		histlen=6
		phlm = PlayHistListMaker.PlayHistListMaker()
		phlm.GetRecentPlays(histlen)
		try:
			ph = phlm.GetPlayHist(0)
		except:
			print "No Info to Display, run the daemon.\n"
			import sys
			sys.exit(0)
		currelay = int(self.configdb.GetConfigItem("current_relay"))
		cursong = int(self.configdb.GetConfigItem("current_song"))
		haverelay=0
		havesong=0
		if currelay != 0 and cursong == 0:
			haverelay=1
			import HaloRadio.Relay as Relay
			r = Relay.Relay(currelay)
			context.addGlobal ("currelay",r.GetDisplayName()) 
			context.addGlobal ("killurl", "%s?action=kill&songid=0" % ( self.config['general.cgi_url']) )
 			refresh_delay = 150
		else:
			havesong=1
			cur_song = ph.GetSong()
		
			if ph.requestby !=0:
				u = User.User(ph.requestby)
				curreqby = u.GetDisplayName()
			else:
				curreqby = ""

			context.addGlobal ("cursngurl", "%s?action=songInfo&id=%d"%( self.config['general.cgi_url'], cur_song.id))
			context.addGlobal ("cursng", cur_song.GetDisplayName())
			context.addGlobal ("killurl", "%s?action=kill&songid=%d" % ( self.config['general.cgi_url'],cur_song.id) )
			context.addGlobal ("curreqby", curreqby)
			context.addGlobal ("curlength", cur_song.GetDisplayLength())
			curprcnt = int(self.configdb.GetConfigItem("current_percent"))
		
			seen = cur_song.mpeg_length * curprcnt / 100
 			refresh_delay = int(int( cur_song.mpeg_length) - seen )
			if refresh_delay < 0:
				refresh_delay = 150
			context.addGlobal ("curprcnt", curprcnt )
		if i < 25:
			context.addGlobal ("refresh_delay", "%d;URL=%s?action=CurrentInfo&i=%d"% ( refresh_delay, self.config['general.cgi_url'], i ) )
		else:
			context.addGlobal ("refresh_delay", " ")
		context.addGlobal ("haverelay", haverelay)
		context.addGlobal ("havesong", havesong)
		prevsngs = []


		for i in range(1,histlen):
			try:
				ph = phlm.GetPlayHist(i)
			except:
				continue
			if ph.requestby !=0:
				u = User.User(ph.requestby)
				curreqby = u.GetDisplayName()
			else:
				curreqby = ""

			try:
				cur_song = ph.GetSong()
			except Exception.SongNotFound:
				continue
			listitem = {}
			listitem['sngurl']="%s?action=songInfo&id=%d"%(
				self.config['general.cgi_url'], cur_song.id )
			listitem['sng']=cur_song.GetDisplayName()
			listitem['reqby']=curreqby
			prevsngs.append(listitem)
		context.addGlobal ("prevsngs", prevsngs)
		context.addGlobal (
		   "playhisturl", "%s?action=playHistory"%(
		      self.config['general.cgi_url']
		    )
		  )
		havenextsng = 0
		rlm = RequestListMaker.RequestListMaker()
		rlm.Get()
		if len(rlm.list) != 0:
			havenextsng = 1
			r = rlm.GetRequest(0)
			s = r.GetSong()
			u = User.User(r.requestby)
			context.addGlobal ("nextsng", s.GetDisplayName())
			context.addGlobal ("nextsngurl", 
				"%s?action=songInfo&id=%d"%(
				self.config['general.cgi_url'], s.id ))
			context.addGlobal ("nextsngreqby", u.GetDisplayName())
			context.addGlobal ("nextlength", s.GetDisplayLength())
		context.addGlobal ("havenextsng", havenextsng)

		# Active Users
		active_users=[]
		slm = SessionListMaker.SessionListMaker()
		slm.GetActive()
		for i in range(0,len(slm.list)):
			user={}
			s = slm.GetSession(i)
			u = s.GetUser()
			user['name'] = u.GetDisplayName()
			if u.id == 1 or self.do_authorize(self.user.rights, "am"): # Annymous Guest, eh ?
				user['host'] = s.host
			user['last_active'] = s.GetActivity()
			active_users.append(user)
		context.addGlobal ( "active_users", active_users )
