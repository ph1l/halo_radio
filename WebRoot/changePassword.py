import HaloRadio.TopWeb as TopWeb
class plugin(TopWeb.TopWeb):
        def GetReqs(self):
                return "amvU"
	def handler(self, context):
		
		context.addGlobal ("formaction", self.config['general.cgi_url'])
