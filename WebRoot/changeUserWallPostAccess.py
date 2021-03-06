import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "am"
	def handler(self, context):
		import string
		if self.form.has_key("id"):
			userid = int(self.form['id'].value)

		import HaloRadio.User as User

		try:
			u = User.User(userid)
		except:
			self.do_error("user doesn't exist")
		
		if (self.do_authorize(self.user.rights, "a")):
			u.ChangePostAccess()
		elif (self.configdb.GetConfigItem('moderator_wall_enable_access') == "1" and
			self.do_authorize(self.user.rights, "m") and
			not self.do_authorize(u.rights,"a") and
			not self.do_authorize(u.rights,"m")
		):
			u.ChangePostAccess()

		request_url = "%s?action=UserList" % ( self.config['general.cgi_url'] )
		context.addGlobal ("refresh", "0;URL=%s" % ( request_url ) )
		context.addGlobal ("requesturl", request_url )


