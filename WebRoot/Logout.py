import HaloRadio.TopWeb as TopWeb
import HaloRadio.Request as Request
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amvU"

	def handler(self, context):
		import HaloRadio.User as User
		# do access checks here :

		u = User.User(1)
		self.session.SetUser(u)

		refresh_url = "%s?action=Welcome" % ( self.config['general.cgi_url'] )

		context.addGlobal ("refresh", "0;URL=%s" % ( refresh_url ) )
		context.addGlobal ("refreshurl", refresh_url )


