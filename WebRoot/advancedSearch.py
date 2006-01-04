import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
		if self.config['general.guest_has_request'] == "1":
                	return "amvUG"
		else:
			return "amv"
	def handler(self, context):
		import HaloRadio.User as User
		import HaloRadio.UserListMaker as UserListMaker

                if self.form.has_key("days"):
                        days = int(self.form['days'].value)
                else:
                        days = 7
		context.addGlobal ("days", days)

		ulm = UserListMaker.UserListMaker()
		ulm.GetAll()
		users = []
		for userid in ulm.list:
			user = User.User(userid)
			entity = {}
			entity['username'] = user.GetDisplayName()
			users.append(entity)

		fields = []
		for field in ['path','artist','album','title']:
			entity = {}
			entity['fieldname'] = field
			fields.append(entity)

		context.addGlobal ("fieldlist", fields)
		context.addGlobal ("userlist", users)
		context.addGlobal ("formaction", self.config['general.cgi_url'])

