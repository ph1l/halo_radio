import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amv"
	def handler(self, context):
		import HaloRadio.UserListMaker as UserListMaker
		import HaloRadio.User as User

		ulm = UserListMaker.UserListMaker()
		ulm.GetAll()
		users = []
		if (self.do_authorize(self.user.rights, "a")):
			is_admin=1
		else:
			is_admin=0
		context.addGlobal ("is_admin", is_admin)
		for userid in ulm.list:
			user = User.User(userid)
			entity = {}
			entity['userid'] = user.id
			entity['userlink'] = "%s?action=userInfo&id=%s" % ( self.config['general.cgi_url'], user.id )
			entity['username'] = user.GetDisplayName()
			entity['editlink'] = "%s?action=editUser&id=%s" % ( self.config['general.cgi_url'], user.id )
			entity['deletelink'] = "%s?action=deleteUserPost&id=%s" % ( self.config['general.cgi_url'], user.id )

			if is_admin:
				entity['email'] = user.email
				entity['mailto'] = "mailto:%s"%(user.email)
			else:
				entity['email'] = "<hidden>"
				entity['mailto'] = ""

			
			entity['rights'] = user.rights
			entity['requests'] = user.requests
			entity['kills'] = user.kills
			
			users.append(entity)
		context.addGlobal ("userlist", users)

