import HaloRadio.TopWeb as TopWeb
import HaloRadio.RequestListMaker as RequestListMaker
import HaloRadio.User as User

class plugin(TopWeb.TopWeb):
        def GetReqs(self):
		if self.config['general.guest_has_request'] == "1":
			return "amvUG"
		else:
			return "amv"

	def handler(self, context):
		rlm=RequestListMaker.RequestListMaker()

		if (self.do_authorize(self.user.rights, "a") or self.do_authorize(self.user.rights, "m")):
			is_admin=1
		else:
			is_admin=0
		context.addGlobal ("is_admin", is_admin)
		context.addGlobal ("formaction", self.config['general.cgi_url'])
		requestlist = []

		# release conditions
		rlm.GetHeld()
		myheldrequests = 0
		if len(rlm.list):
			rlm.GetByUserHeld(self.user.id)
			if len(rlm.list) or is_admin:
				context.addGlobal ("releaserequestscondition", 1)
				context.addGlobal ("viewalllinkcondition", 1)
				myheldrequests = len(rlm.list)
				context.addGlobal ("heldrequests", myheldrequests)

		# viewall conditions
		viewall = ""
		myrequests = 0
		if self.form.has_key("viewall"):
			viewall = "&viewall=1"
			context.addGlobal ("viewall",1)
			context.addGlobal ("viewalllinkcondition", 0)
			rlm.GetAllHeld()
		else:
			myrequests = myheldrequests
			context.addGlobal ("viewalllink", self.config['general.cgi_url'] + "?action=RequestQueue&viewall=1")
			rlm.GetAll()

		context.addGlobal ("numrequests", len(rlm.list))
		if len(rlm.list) == 0:
			context.addGlobal ("requestlist", requestlist)
			if is_admin and viewall == "" and myheldrequests < 1:
				context.addGlobal ("releaserequestscondition", 0)
			return
			
		firstreq = rlm.list[0]
		heldrequests = 0
		total_length = 0
		for i in range( 0, len(rlm.list)):
			curreq = rlm.GetRequest( i )
			prevreq = rlm.GetRequest( i-1 )
			try:
				nextreq = rlm.GetRequest( i+1 )
			except:
				nextreq = rlm.GetRequest( 0 )
			song = curreq.GetSong()
			user = User.User(curreq.requestby)
			request={}
			if curreq.hold == 0:
				request['classname'] = "resultsrow"
				request['held'] = 0
			else:
				request['classname'] = "resultsrowdark"
				request['held'] = 1
			if curreq.requestby == self.user.id or is_admin:
				myrequests += 1
				if curreq.hold:
					heldrequests += 1
			request['curid'] = curreq.id
			request['downurl'] = "%s?action=swapRequests&reqid=%s&swapid=%s%s" % (self.config['general.cgi_url'], curreq.id, nextreq.id, viewall )
			request['upurl'] = "%s?action=swapRequests&reqid=%s&swapid=%s%s" % (self.config['general.cgi_url'], curreq.id, prevreq.id, viewall )
			request['by'] = user.GetDisplayName()
			request['song'] = song.GetDisplayName()
			request['songurl'] = "%s?action=songInfo&id=%d"%( self.config['general.cgi_url'], song.id)
			request['songlen'] = song.GetDisplayLength()
			total_length += song.mpeg_length
			requestlist.append(request)
		context.addGlobal ("classname", "resultsrow")
		context.addGlobal ("total_song_legnth", "%02d:%02d" % ( total_length / 60, total_length % 60 ))

		context.addGlobal ("requestlist", requestlist)
		if (myrequests - heldrequests) > 0:
			context.addGlobal ("holdrequestscondition", 1)
		if myrequests or is_admin:
			context.addGlobal ("deletecondition", 1)
		if is_admin:
			context.addGlobal ("zipcondition", 1)
		if is_admin and viewall == "" and myheldrequests < 1:
			context.addGlobal ("releaserequestscondition", 0)
