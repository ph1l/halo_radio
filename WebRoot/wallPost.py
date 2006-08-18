import HaloRadio.TopWeb as TopWeb
import HaloRadio.Request as Request
import HaloRadio.User as User
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amv"
	def handler(self, context):
		import HaloRadio.Wall as Wall
		if self.form.has_key("line"):
			line = self.form['line'].value
		u = User.User(self.session.userid)
		if not u.GetPostAccess():
			self.do_error("You do not have access to post to the wall.")
		
		w = Wall.Wall(0,self.session.userid,line)

		refresh_url = "%s?action=Wall" % ( self.config['general.cgi_url'] )

		context.addGlobal ("refresh", "1;URL=%s" % ( refresh_url ) )
		context.addGlobal ("refreshurl", refresh_url )


