import HaloRadio.TopWeb as TopWeb
import HaloRadio.Request as Request
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "a"
	def handler(self, context):
		import HaloRadio.Config as Config

		if self.form.has_key("playlist"):
			playlist = str(int(self.form['playlist'].value))

		cfg = Config.Config()

		cfg.SetConfigItem("current_list",playlist)
		
		request_url = "%s?action=Admin" % ( self.config['general.cgi_url'] )

		context.addGlobal ("refresh", "0;URL=%s" % ( request_url ) )
		context.addGlobal ("requesturl", request_url )


