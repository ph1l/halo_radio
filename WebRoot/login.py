import HaloRadio.TopWeb as TopWeb
import HaloRadio.Request as Request
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "G"
	def handler(self, context):
		import HaloRadio.User as User
		user = None
		password = None
		if self.form.has_key("user"):
			user = self.form['user'].value
		if self.form.has_key("password"):
			password = self.form['password'].value
		# do access checks here :

		if user == None or password == None:
			self.do_error("username and password fields must be filled in")
		self.session.Authenticate(user, password)

		refresh_url = "%s?action=Welcome" % ( self.config['general.cgi_url'] )

		context.addGlobal ("refresh", "1;URL=%s" % ( refresh_url ) )
		context.addGlobal ("refreshurl", refresh_url )


