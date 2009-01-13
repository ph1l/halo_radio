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
		is_admin=0
		enable=0
		wall_enable=0
		if (self.do_authorize(self.user.rights, "a")):
			is_admin=1
			enable=1
			wall_enable=1
		elif self.do_authorize(self.user.rights, "m"):
			is_admin=0
			enable=0
			wall_enable=0
			if self.configdb.GetConfigItem('moderator_enable_access') == "1":
				enable=1
			if self.configdb.GetConfigItem('moderator_wall_enable_access') == "1":
				wall_enable=1
		context.addGlobal ("is_admin", is_admin)
		context.addGlobal ("enable", enable)
		context.addGlobal ("wall_enable", wall_enable)
		for userid in ulm.list:
			user = User.User(userid)
			entity = {}
			entity['userid'] = user.id
			entity['userlink'] = "%s?action=userInfo&id=%s" % ( self.config['general.cgi_url'], user.id )
			entity['username'] = user.GetDisplayName()
			entity['editlink'] = "%s?action=Preferences&id=%s" % ( self.config['general.cgi_url'], user.id )
			entity['wallenablelink'] = "%s?action=changeUserWallPostAccess&id=%s" % ( self.config['general.cgi_url'], user.id )
			entity['enablelink'] = "%s?action=changeUserAccess&id=%s" % ( self.config['general.cgi_url'], user.id )

			entity['email'] = "<hidden>"
			entity['mailto'] = ""
			if is_admin:
				entity['email'] = user.email
				entity['mailto'] = "mailto:%s"%(user.email)
			if enable:
				if user.GetAccess():
					entity['enabled'] = "enabled"
					entity['class'] = "resultsrow"
				else:
					entity['enabled'] = "disabled"
					entity['class'] = "resultsrowdark"
			if wall_enable:
				if user.GetPostAccess():
					entity['wallenabled'] = "enabled"
					entity['wallclass'] = "resultsrow"
				else:
					entity['wallenabled'] = "disabled"
					entity['wallclass'] = "resultsrowdark"

			
			entity['rights'] = user.rights
			entity['requests'] = user.requests
			entity['kills'] = user.kills
			
			users.append(entity)
		context.addGlobal ("userlist", users)

