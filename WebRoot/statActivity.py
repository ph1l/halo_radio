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
		import HaloRadio.UserListMaker as UserListMaker
		import HaloRadio.User as User
		import datetime, time
		from operator import itemgetter
		users=[]
		ACTIVITY_TIMEOUT = 2592000
		ulm = UserListMaker.UserListMaker()
		ulm.GetAll()
		for user_id in ulm.list:
			u= User.User(user_id)
			if u.name == "Anonymous":
				continue
			last_seen = u.LastSeen()
			now = time.mktime(datetime.datetime.now().timetuple())
			if time.mktime(last_seen.timetuple()) > now -ACTIVITY_TIMEOUT:
				entity={}
				entity['username']=u.name
				entity['userlink']="%s?action=userInfo&id=%s" % ( self.config['general.cgi_url'], u.id )
				entity['seen_on']=u.LastSeen()
				users.append(entity)
		sorted_users = sorted(users, key=itemgetter('seen_on'))
		sorted_users.reverse()
		context.addGlobal ("users", sorted_users)


