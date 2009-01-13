import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amvUG"
	def handler(self, context):
		import HaloRadio.Util as Util

		context.addGlobal ("listeners", Util.GetListeners())

		graphlist =[]
		timelist=('daily','weekly','monthly','yearly')
		#timelist=('daily','weekly', 'monthly')

		for time in timelist:
			entity={}
			entity['url']="%s/halostat--activity-%s.png" % (self.config['general.root_url'], time)
			graphlist.append(entity)
		context.addGlobal ("graphs", graphlist)

		# Recently Active Users
		import HaloRadio.SessionListMaker as SessionListMaker
		import HaloRadio.Session as Session
		slm = SessionListMaker.SessionListMaker()
		users=[]
		slm.GetActive(10080)
		for session_id in slm.list:
			s= Session.Session(session_id)
			u = s.GetUser()
			entity={}
			entity['username']=u.name
			entity['userlink']="%s?action=userInfo&id=%s" % ( self.config['general.cgi_url'], u.id )
			entity['seen_on']=s.GetActivity()
			users.append(entity)
		context.addGlobal ("users", users)


