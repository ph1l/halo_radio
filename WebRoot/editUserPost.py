import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amv"
	def handler(self, context):
		import string
		username = None
		rights = None
		email = None
		passwd = None
		style = None
		if self.form.has_key("userid"):
			userid = int(self.form['userid'].value)
		if self.form.has_key("username"):
			username = self.form['username'].value
		if self.form.has_key("rights"):
			rights = self.form['rights'].value
		if self.form.has_key("email"):
			email = self.form['email'].value
		if self.form.has_key("passwd"):
			passwd = self.form['passwd'].value
		if self.form.has_key("style"):
			style = self.form['style'].value
			style = int(style)

		import HaloRadio.User as User

		try:
			u = User.User(userid)
		except:
			self.do_error("user doesn't exist")
		
		if (self.do_authorize(self.user.rights, "a")):
			if len(rights) < 1:
				self.do_error("you are required to give them something")
			u.SetPassword(passwd)
			u.UpdateRights(rights)
			u.UpdateName(username)
			u.UpdateEmail(email)
			u.UpdateStyle(style)
		elif (self.do_authorize(self.user.rights, "m") and
			not self.do_authorize(u.rights,"a") and
			not self.do_authorize(rights, "a")
		):
			if len(rights) < 1:
				self.do_error("you are required to give them something")
			u.UpdateRights(rights)
			u.UpdateName(username)
			u.UpdateEmail(email)
			u.UpdateStyle(style)
		if (self.user.id == userid):
			u.UpdateStyle(style)
			u.SetPassword(passwd)


		request_url = "%s?action=Preferences&id=%d" % ( self.config['general.cgi_url'], userid )
		context.addGlobal ("refresh", "0;URL=%s" % ( request_url ) )
		context.addGlobal ("requesturl", request_url )


