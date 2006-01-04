import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amvU"
	def handler(self, context):
		import string
		if self.form.has_key("pass"):
			passwd = self.form['pass'].value
		if self.form.has_key("pass2"):
			passwd2 = self.form['pass2'].value

		if len(passwd) < 4:
			self.do_error("password must be greater than 4 characters.")

		if passwd != passwd2:
			self.do_error("passwords don't match")


		self.user.SetPassword(passwd)

                request_url = "%s?action=Welcome" % ( self.config['general.cgi_url'] )

                context.addGlobal ("refresh", "0;URL=%s" % ( request_url ) )
                context.addGlobal ("requesturl", request_url )

