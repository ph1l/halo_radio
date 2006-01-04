import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amvUG"
	def handler(self, context):
		import string
		if self.form.has_key("user"):
			user = self.form['user'].value
		if self.form.has_key("hash"):
			userhash = self.form['hash'].value

		import HaloRadio.User as User
		import HaloRadio.UserListMaker as UserListMaker

		#try:
		ulm = UserListMaker.UserListMaker()
		ulm.GetByName(user)
		u = ulm.GetUser(0)
		#except:
		#	self.do_error("user doesn't exist.")

		dbhash = u.GetHash()	

		if userhash == dbhash:
			self.session.SetUser(u)
			u = self.session.GetUser()
			u.ClearHash()
		else:
			self.do_error("verify hash incorrect")

                request_url = "%s?action=changePassword" % ( self.config['general.cgi_url'] )

                context.addGlobal ("refresh", "0;URL=%s" % ( request_url ) )
                context.addGlobal ("requesturl", request_url )

