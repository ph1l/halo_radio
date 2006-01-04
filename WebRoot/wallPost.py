import HaloRadio.TopWeb as TopWeb
import HaloRadio.Request as Request
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amv"
	def handler(self, context):
		import HaloRadio.Wall as Wall
		if self.form.has_key("line"):
			line = self.form['line'].value
		
		w = Wall.Wall(0,self.session.userid,line)

		refresh_url = "%s?action=Wall" % ( self.config['general.cgi_url'] )

		context.addGlobal ("refresh", "1;URL=%s" % ( refresh_url ) )
		context.addGlobal ("refreshurl", refresh_url )


